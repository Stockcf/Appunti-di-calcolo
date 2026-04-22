from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDFS = [
    ROOT / "Dispensa11-12.pdf",
    ROOT / "Metodi_Numerici_per_l'Algebra_Lineare.pdf",
]
DEFAULT_CHAPTERS = [
    ROOT / "Chapters" / "ch01" / "chapter01.tex",
    ROOT / "Chapters" / "ch02" / "chapter02.tex",
    ROOT / "Chapters" / "appendice" / "appendice.tex",
]
OUTPUT_DIR = ROOT / "reports"
OUTPUT_FILE = OUTPUT_DIR / "brief_agente_appunti.md"
CHAPTER_TARGETS = {
    "ch01": ROOT / "Chapters" / "ch01" / "chapter01.tex",
    "ch02": ROOT / "Chapters" / "ch02" / "chapter02.tex",
    "ch03": ROOT / "Chapters" / "ch03" / "chapter03.tex",
    "appendice": ROOT / "Chapters" / "appendice" / "appendice.tex",
}

STOPWORDS = {
    "della",
    "delle",
    "degli",
    "dello",
    "numerico",
    "numerici",
    "metodo",
    "metodi",
    "teorema",
    "teoremi",
    "definizione",
    "definizioni",
    "capitolo",
    "appendice",
    "sistemi",
    "lineari",
    "calcolo",
}


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.lower()


def keywords_from_topic(topic: str, limit: int = 10) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9]+", normalize(topic))
    out: list[str] = []
    for w in words:
        if len(w) < 4 or w in STOPWORDS:
            continue
        if w not in out:
            out.append(w)
        if len(out) >= limit:
            break
    return out


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def latex_escape(text: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    out = text
    for old, new in repl.items():
        out = out.replace(old, new)
    return out


def latex_escape_url(url: str) -> str:
    return url.replace("%", r"\%")


def resolve_target_file(chapter: str, target_file: str | None) -> Path:
    if target_file:
        return Path(target_file)
    return CHAPTER_TARGETS.get(chapter, CHAPTER_TARGETS["appendice"])


def extract_style_profile(chapter_paths: list[Path]) -> dict[str, object]:
    all_text = "\n".join(read_text(p) for p in chapter_paths if p.exists())

    environments = ["defi", "theorem", "prop", "cor", "example", "exercise", "obs", "axioma"]
    env_count = {
        env: len(re.findall(rf"\\begin\{{{env}\}}", all_text))
        for env in environments
    }

    section_count = len(re.findall(r"\\section\{", all_text))
    subsection_count = len(re.findall(r"\\subsection\{", all_text))

    top_envs = sorted(env_count.items(), key=lambda x: x[1], reverse=True)
    top_envs = [env for env, count in top_envs if count > 0][:4]

    return {
        "sections": section_count,
        "subsections": subsection_count,
        "environments": env_count,
        "preferred_environments": top_envs,
        "notes": [
            "Mantieni catena: definizione -> risultato -> esempio.",
            "Per gli algoritmi esplicita ipotesi, arresto e costo.",
            "Conserva notazione coerente tra capitoli.",
        ],
    }


def extract_pdf_snippets(pdf_paths: list[Path], keywords: list[str], max_pages: int = 10) -> list[dict[str, str]]:
    snippets: list[dict[str, str]] = []
    ranked: list[tuple[int, dict[str, str]]] = []

    try:
        from pypdf import PdfReader
    except Exception:
        return [
            {
                "source": "system",
                "snippet": "pypdf non installato. Installa con: pip install pypdf",
            }
        ]

    for pdf in pdf_paths:
        if not pdf.exists():
            continue

        try:
            reader = PdfReader(str(pdf))
        except Exception as exc:
            snippets.append({"source": str(pdf.name), "snippet": f"Errore lettura PDF: {exc}"})
            continue

        pages_to_scan = min(len(reader.pages), max_pages)
        for page_idx in range(pages_to_scan):
            page_text = (reader.pages[page_idx].extract_text() or "").replace("\n", " ")
            norm = normalize(page_text)

            score = sum(norm.count(k) for k in keywords) if keywords else 1
            if keywords and score == 0:
                continue

            excerpt = " ".join(page_text.split())
            if len(excerpt) > 320:
                excerpt = excerpt[:320] + "..."
            ranked.append(
                (
                    score,
                    {
                        "source": f"{pdf.name} p.{page_idx + 1}",
                        "snippet": excerpt,
                    },
                )
            )

    ranked.sort(key=lambda x: x[0], reverse=True)
    for _, item in ranked[:12]:
        snippets.append(item)

    return snippets


def fetch_wikipedia_summary(topic: str, lang: str = "it") -> dict[str, str]:
    title = quote(topic.replace(" ", "_"))
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"

    try:
        with urlopen(url, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8", errors="ignore"))
    except URLError as exc:
        return {
            "title": "Wikipedia",
            "url": url,
            "summary": f"Nessuna risposta online ({exc}).",
        }
    except Exception as exc:
        return {
            "title": "Wikipedia",
            "url": url,
            "summary": f"Errore ricerca online: {exc}",
        }

    summary = payload.get("extract", "Nessun estratto disponibile.")
    page_url = payload.get("content_urls", {}).get("desktop", {}).get("page", url)
    title_out = payload.get("title", topic)

    return {
        "title": title_out,
        "url": page_url,
        "summary": summary,
    }


def collect_context(topic: str) -> dict[str, object]:
    keywords = keywords_from_topic(topic)
    style_profile = extract_style_profile(DEFAULT_CHAPTERS)
    pdf_snippets = extract_pdf_snippets(DEFAULT_PDFS, keywords)
    wiki = fetch_wikipedia_summary(topic)
    return {
        "keywords": keywords,
        "style_profile": style_profile,
        "pdf_snippets": pdf_snippets,
        "wiki": wiki,
    }


def build_brief(topic: str, chapter: str, detail: str, context: dict[str, object]) -> str:
    keywords = context["keywords"]
    style_profile = context["style_profile"]
    pdf_snippets = context["pdf_snippets"]
    wiki = context["wiki"]

    lines: list[str] = []
    lines.append("# Brief per agente appunti")
    lines.append("")
    lines.append(f"- Argomento: {topic}")
    lines.append(f"- Capitolo target: {chapter}")
    lines.append(f"- Livello dettaglio: {detail}")
    lines.append(f"- Parole chiave: {', '.join(keywords) if keywords else 'n/a'}")
    lines.append("")

    lines.append("## Profilo stile locale")
    lines.append(f"- Sezioni trovate: {style_profile['sections']}")
    lines.append(f"- Sottosezioni trovate: {style_profile['subsections']}")
    preferred = style_profile.get("preferred_environments", [])
    lines.append(f"- Ambienti preferiti: {', '.join(preferred) if preferred else 'n/a'}")
    for note in style_profile.get("notes", []):
        lines.append(f"- {note}")
    lines.append("")

    lines.append("## Evidenze da PDF")
    if pdf_snippets:
        for snip in pdf_snippets:
            lines.append(f"- Fonte: {snip['source']}")
            lines.append(f"  Estratto: {snip['snippet']}")
    else:
        lines.append("- Nessun estratto rilevante trovato nelle prime pagine scansionate.")
    lines.append("")

    lines.append("## Integrazione online")
    lines.append(f"- Fonte: {wiki['title']}")
    lines.append(f"- URL: {wiki['url']}")
    lines.append(f"- Sintesi: {wiki['summary']}")
    lines.append("")

    lines.append("## Prompt operativo per Copilot")
    lines.append(
        "Scrivi una sezione LaTeX per appunti di Calcolo Numerico in stile coerente col repository. "
        "Usa prima le evidenze PDF, integra il minimo necessario dalla fonte online, e segui lo schema "
        "definizione -> proprieta/teorema -> esempio numerico. Se tratti un metodo, includi ipotesi, "
        "algoritmo, criterio di arresto e costo. Mantieni notazione coerente con i capitoli esistenti."
    )

    return "\n".join(lines)


def build_latex_draft(topic: str, chapter: str, detail: str, context: dict[str, object]) -> str:
    wiki = context["wiki"]
    snippet_lines: list[str] = []
    for snip in context["pdf_snippets"][:2]:
        source = latex_escape(str(snip["source"]))
        text = latex_escape(str(snip["snippet"]))
        snippet_lines.append(f"\\item \\textbf{{{source}}}: {text}")

    section_title = latex_escape(topic.strip().capitalize())
    detail_map = {
        "breve": "Sintesi essenziale con formula principale.",
        "medio": "Sviluppo completo con formula, proprieta e passaggi essenziali.",
        "esteso": "Sviluppo esteso con osservazioni su stabilita e condizionamento.",
    }
    detail_note = detail_map.get(detail, detail_map["medio"])
    wiki_title = latex_escape(str(wiki["title"]))
    wiki_url = latex_escape_url(str(wiki["url"]))

    lines: list[str] = []
    lines.append(f"% ---- BOZZA AGENTE ({chapter}) ----")
    lines.append(f"\\section{{{section_title}}}")
    lines.append("")
    lines.append("\\begin{defi}[Impostazione del problema]")
    lines.append(
        f"Si consideri il problema legato a \\textbf{{{latex_escape(topic)}}}. "
        "Si fissano ipotesi e notazione coerenti con i capitoli precedenti."
    )
    lines.append("\\end{defi}")
    lines.append("")
    lines.append("\\begin{theorem}[Proprieta operativa]")
    lines.append(
        "Sotto ipotesi standard di regolarita, il metodo/risultato ammette una formulazione "
        "numericamente trattabile; si valutano stabilita e sensibilita dei dati."
    )
    lines.append("\\end{theorem}")
    lines.append("")
    lines.append("\\begin{obs}")
    lines.append("Per la parte algoritmica esplicitare sempre:")
    lines.append("\\begin{itemize}")
    lines.append("    \\item ipotesi di applicabilita;")
    lines.append("    \\item passi principali dell'algoritmo;")
    lines.append("    \\item criterio di arresto;")
    lines.append("    \\item costo computazionale dominante.")
    lines.append("\\end{itemize}")
    lines.append("\\end{obs}")
    lines.append("")
    lines.append("\\begin{example}[Esempio numerico guida]")
    lines.append(
        "Inserire un esempio numerico completo (preferibilmente di piccola dimensione), "
        "mostrando i passaggi e commentando eventuali effetti di arrotondamento."
    )
    lines.append(f"{detail_note}")
    lines.append("\\end{example}")
    lines.append("")
    if snippet_lines:
        lines.append("\\begin{obs}[Tracce utili dalle dispense]")
        lines.append("\\begin{itemize}")
        lines.extend(snippet_lines)
        lines.append("\\end{itemize}")
        lines.append("\\end{obs}")
        lines.append("")

    lines.append("\\begin{obs}[Integrazione online]")
    lines.append(f"Riferimento di supporto: \\textbf{{{wiki_title}}}, \\url{{{wiki_url}}}.")
    lines.append("\\end{obs}")
    lines.append("")

    return "\n".join(lines)


def append_draft(target_path: Path, draft: str) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists():
        original = target_path.read_text(encoding="utf-8", errors="ignore")
        sep = "\n\n" if original and not original.endswith("\n") else "\n"
        target_path.write_text(original + sep + draft + "\n", encoding="utf-8")
        return
    target_path.write_text(draft + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepara un brief per un agente di scrittura appunti (PDF + web + stile locale)."
    )
    parser.add_argument("--topic", required=True, help="Argomento da sviluppare")
    parser.add_argument("--chapter", default="appendice", help="Capitolo target")
    parser.add_argument(
        "--detail",
        default="medio",
        choices=["breve", "medio", "esteso"],
        help="Livello di dettaglio richiesto",
    )
    parser.add_argument(
        "--out",
        default=str(OUTPUT_FILE),
        help="Percorso output markdown",
    )
    parser.add_argument(
        "--write-draft",
        action="store_true",
        help="Genera e appende una bozza LaTeX nel capitolo target.",
    )
    parser.add_argument(
        "--target-file",
        default=None,
        help="File .tex target (se omesso usa la mappa del capitolo).",
    )

    args = parser.parse_args()

    context = collect_context(args.topic)
    brief = build_brief(args.topic, args.chapter, args.detail, context)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(brief, encoding="utf-8")

    print(f"Brief generato: {out_path}")

    if args.write_draft:
        draft = build_latex_draft(args.topic, args.chapter, args.detail, context)
        target_path = resolve_target_file(args.chapter, args.target_file)
        append_draft(target_path, draft)
        print(f"Bozza LaTeX aggiunta in: {target_path}")


if __name__ == "__main__":
    main()
