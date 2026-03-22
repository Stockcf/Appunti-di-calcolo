# Appunti di Calcolo Numerico

**Autore:** R. Castagni Fabbri

Questa repository contiene una raccolta di appunti di Calcolo Numerico, scritti in LaTeX e organizzati in capitoli modulari.
Il progetto è stato inizialmente sviluppato a partire da una repository trovata su GitHub (https://github.com/YuriODev/MathsCodeBook?tab=CC0-1.0-1-ov-file).

Se ti interessa solo il PDF, puoi visualizzarlo o scaricarlo direttamente qui:
[📥 Scarica main.pdf](https://github.com/Stockcf/Appunti-di-calcolo/raw/main/main.pdf)

*(gli appunti sono in fase di scrittura, verranno terminate nel corso dell'AA 25/26)*


## 📁 Struttura del Progetto

```
.
├── main.tex                 # File principale LaTeX
├── styles.cls              # Classe LaTeX personalizzata per il design
├── README.md              # Questo file
└── Chapters/
    └── ch01/              # Capitolo Template
        ├── chapter01.tex
        ├── code/           # (Opzionale) Implementazioni in Python/C++
        └── graphics/       # (Opzionale) Visualizzazioni (grafici TikZ)

```

## 🏗️ Come Iniziare

### 1. **Compilare il Progetto**
   - Utilizza un compilatore LaTeX (es. pdflatex, xelatex, lualatex):
   ```bash
   pdflatex main.tex
   ```
   - Genera: `main.pdf`

### 2. **Aggiungere un Nuovo Capitolo**
   - Crea una nuova cartella: `Chapters/ch02/`
   - Crea il file: `Chapters/ch02/chapter02.tex`
   - Aggiungi in `main.tex`:
   ```latex
   \include{Chapters/ch02/chapter02}  % Chapter 2: Titolo dell'argomento
   ```

### 3. **Modificare il Capitolo Template**
   - Apri [Chapters/ch01/chapter01.tex](Chapters/ch01/chapter01.tex)
   - Sostituisci i testi di esempio con il tuo contenuto
   - Usa gli ambienti LaTeX disponibili per strutturare il capitolo

## 📝 Elementi LaTeX Disponibili

### Ambienti per Definizioni e Teoremi
- `\begin{defi}[Nome]` - Definizioni
- `\begin{theorem}[Nome]` - Teoremi
- `\begin{prop}[Nome]` - Proposizioni
- `\begin{cor}[Nome]` - Corollari
- `\begin{exercise}` - Esercizi
- `\begin{example}` - Esempi
- `\begin{obs}` - Osservazioni
- `\begin{axioma}[Nome]` - Assiomi

Tutti gli ambienti sono racchiusi in **scatole colorate** per una lettura facile.

## 🎨 Personalizzazione

### Modificare i Colori
Nel `main.tex`, modifica:
```latex
\definecolor{colorp}{cmyk}{0.81,0.62,0.00,0.22}
\definecolor{colordef}{cmyk}{0.81,0.62,0.00,0.22}
```

### Cambiare il Font
Nel `main.tex`:
```latex
\customfont{Montserrat}  % Opzioni: Montserrat, MathPazo, ecc.
```

### Cambiare il Titolo del Libro
Nel `main.tex`:
```latex
\booktitle{Appunti di Calcolo Numerico}
\subtitle[:]{Università di Pisa - Ingegneria dell'energia}
```

## 📖 Template per una Nuova Sezione

```latex
\section{Titolo della Sezione}

\subsection{Sottosezione}

\begin{defi}[Nome Definizione]
Testo della definizione con formula: $f(x) = x^2$
\end{defi}

\begin{theorem}[Nome Teorema]
Enunciato del teorema con formula:
\[
\int_a^b f(x) \, dx = F(b) - F(a)
\]
\end{theorem}

\begin{example}
Descrizione dell'esempio e della soluzione.
\end{example}

\begin{exercise}
Testo dell'esercizio.
\end{exercise}
```

## 🔧 Requisiti

- **LaTeX Distribution**: TeX Live, MikTeX, o MacTeX
- **Compiler**: pdflatex, xelatex, o lualatex
- **Font**: Montserrat (scarica da Google Fonts se non disponibile)

## 💡 Note

- **Codesnippet disabilitato**: Per aggiungere codice sorgente, copia il codice direttamente nel documento o usa ambienti `listings` di LaTeX.
- **Struttura semplificata**: Il progetto non include grafici TikZ e code snippets per mantenere la semplicità. Aggiungili secondo le necessità.

---

**Data di Creazione:** Marzo 2026  
**Ultimo Aggiornamento:** Marzo 2026
