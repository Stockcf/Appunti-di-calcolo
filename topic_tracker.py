#!/usr/bin/env python3
"""
Topic Tracker for Numerical Calculus Notes
Tracks which lecture topics are covered in the written notes and which are pending.
"""

import re
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Set, Dict
from enum import Enum


class TopicStatus(Enum):
    """Status of a topic in the documentation"""
    COVERED = "✓"
    PENDING = "○"
    PARTIAL = "◐"


@dataclass
class Topic:
    """Represents a lecture topic"""
    lecture_num: int
    date: str
    lecturer: str
    content: str
    status: TopicStatus = TopicStatus.PENDING

    def extract_keywords(self) -> Set[str]:
        """Extract key topics/keywords from lecture content"""
        # Remove Italian articles and common words
        stopwords = {'di', 'del', 'della', 'da', 'le', 'e', 'o', 'per', 'a', 'al', 'alla', 'in', 'il', 'uno', 'una'}
        
        # Extract capitalized terms and specific technical terms
        words = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', self.content)
        words = [w.lower() for w in words if w.lower() not in stopwords]
        
        return set(words)

    def __str__(self) -> str:
        return f"[{self.status.value}] Lezione {self.lecture_num} ({self.date}) - {self.lecturer[:20]}"


class TopicTracker:
    """Main tracker for managing lecture topics"""
    
    def __init__(self, registro_path: str, chapters_dir: str):
        self.registro_path = Path(registro_path)
        self.chapters_dir = Path(chapters_dir)
        self.topics: List[Topic] = []
        self.chapter_keywords: Dict[int, Set[str]] = {}
        
        self.load_topics()
        self.load_chapter_content()
        self.update_topic_status()

    def load_topics(self):
        """Parse registro.txt and extract topics"""
        if not self.registro_path.exists():
            print(f"Error: {self.registro_path} not found")
            return

        with open(self.registro_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse lectures - format: "N. Date time (hours) lezione: content (LECTURER)"
        pattern = r'(\d+)\.\s+(\w+\s+\d+/\d+/\d+)\s+[\d:]+\s*\(.*?\)\s+lezione:\s*(.*?)\s*\(([^)]+)\)'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            lecture_num = int(match.group(1))
            date = match.group(2)
            lecture_content = match.group(3).strip()
            lecturer = match.group(4).strip()
            
            topic = Topic(lecture_num, date, lecturer, lecture_content)
            self.topics.append(topic)

    def load_chapter_content(self):
        """Extract keywords from written chapters"""
        chapter_dirs = [d for d in self.chapters_dir.iterdir() if d.is_dir() and d.name.startswith('ch')]
        
        for ch_dir in sorted(chapter_dirs):
            ch_num = int(ch_dir.name[2:])
            keywords = set()
            
            tex_files = list(ch_dir.glob('*.tex'))
            for tex_file in tex_files:
                try:
                    with open(tex_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract section/subsection titles
                        titles = re.findall(r'\\(?:chapter|section|subsection)\*?\{([^}]+)\}', content)
                        words = re.findall(r'\b([A-Z][a-z]+(?:\s+[a-z]+)*)\b', ' '.join(titles))
                        keywords.update(w.lower() for w in words)
                except Exception as e:
                    print(f"Warning: Could not read {tex_file}: {e}")
            
            self.chapter_keywords[ch_num] = keywords

    def update_topic_status(self):
        """Update status of topics based on chapter coverage"""
        all_chapter_keywords = set()
        for keywords in self.chapter_keywords.values():
            all_chapter_keywords.update(keywords)

        for topic in self.topics:
            topic_keywords = topic.extract_keywords()
            covered_keywords = topic_keywords & all_chapter_keywords
            
            if len(covered_keywords) > len(topic_keywords) * 0.7:
                topic.status = TopicStatus.COVERED
            elif len(covered_keywords) > 0:
                topic.status = TopicStatus.PARTIAL
            else:
                topic.status = TopicStatus.PENDING

    def print_summary(self):
        """Print summary of topic coverage"""
        print("\n" + "=" * 80)
        print("TOPIC TRACKING SUMMARY")
        print("=" * 80)
        
        covered = sum(1 for t in self.topics if t.status == TopicStatus.COVERED)
        partial = sum(1 for t in self.topics if t.status == TopicStatus.PARTIAL)
        pending = sum(1 for t in self.topics if t.status == TopicStatus.PENDING)
        
        print(f"\nStatistics: {covered} covered, {partial} partial, {pending} pending")
        print(f"Total lectures: {len(self.topics)}\n")
        
        print("COVERED TOPICS:")
        print("-" * 80)
        for topic in self.topics:
            if topic.status == TopicStatus.COVERED:
                print(f"{topic}")

        print("\nPARTIAL TOPICS (partially covered):")
        print("-" * 80)
        for topic in self.topics:
            if topic.status == TopicStatus.PARTIAL:
                print(f"{topic}")

        print("\nPENDING TOPICS (not yet covered):")
        print("-" * 80)
        for topic in self.topics:
            if topic.status == TopicStatus.PENDING:
                print(f"{topic}")
        
        print("\n" + "=" * 80 + "\n")

    def export_json(self, output_file: str = "topic_status.json"):
        """Export tracking data to JSON format"""
        import json
        
        data = {
            "summary": {
                "total": len(self.topics),
                "covered": sum(1 for t in self.topics if t.status == TopicStatus.COVERED),
                "partial": sum(1 for t in self.topics if t.status == TopicStatus.PARTIAL),
                "pending": sum(1 for t in self.topics if t.status == TopicStatus.PENDING),
            },
            "topics": [
                {
                    "lecture": t.lecture_num,
                    "date": t.date,
                    "lecturer": t.lecturer,
                    "status": t.status.name,
                    "content_preview": t.content[:200] + "..." if len(t.content) > 200 else t.content
                }
                for t in self.topics
            ]
        }
        
        output_path = self.registro_path.parent / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Data exported to {output_path}")


if __name__ == "__main__":
    import sys
    
    script_dir = Path(__file__).parent
    registro_file = script_dir / "registro.txt"
    chapters_directory = script_dir / "Chapters"
    
    tracker = TopicTracker(str(registro_file), str(chapters_directory))
    tracker.print_summary()
    tracker.export_json()
