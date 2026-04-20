# 📚 Calcolo Numerico - Intelligent Topic Tracker

A smart system to automatically track which lecture topics from your class notes have been covered in your written documentation and which still need to be addressed.

## 🎯 Problem Solved

You asked: *"Qual è un modo intelligente di tenere traccia degli argomenti che sono già stati aggiunti agli appunti e quelli che sono sempre da trattare?"*

**Solution**: An automated system that compares your lecture registry (`registro.txt`) with your written chapters and provides:
- Visual status indicators (✓ covered, ◐ partial, ○ pending)
- JSON export for programmatic access
- Interactive HTML dashboard
- Detailed coverage analysis

## 📦 What You Get

### 1. **topic_tracker.py** - Core Analyzer
The main Python script that:
- Parses your `registro.txt` file
- Extracts technical keywords from lectures
- Analyzes written chapters in `Chapters/`
- Matches lecture topics to chapter coverage
- Exports detailed status data as JSON

**Features:**
- Automatic keyword extraction
- Intelligent matching algorithm (70% threshold for "covered")
- Generates JSON report with statistics

### 2. **generate_dashboard.py** - Visual Dashboard
Creates an interactive HTML dashboard showing:
- Progress bars for overall coverage
- Statistics (covered/partial/pending counts)
- Color-coded topic lists
- Clickable, organized layout
- Fully responsive design

### 3. **Batch Scripts** for Easy Execution

#### **track_all.bat** (Recommended - All-in-one)
One-click execution that:
1. Runs the topic tracker
2. Generates the HTML dashboard
3. Opens dashboard in your default browser
4. Generates JSON report

#### **run_tracker.bat** (Simple)
Just runs the tracker and displays results in console

## 🚀 How to Use

### Quick Start (Easiest Way)
```
1. Double-click: track_all.bat
2. Watch console output
3. Dashboard automatically opens in your browser
```

### Manual Execution
```cmd
cd "C:\Users\ricca\Desktop\II anno\Calcolo numerico\Appunti di calcolo.worktrees\copilot-worktree-2026-04-20T10-07-37"

REM Run tracker only
python topic_tracker.py

REM Generate dashboard
python generate_dashboard.py dashboard.html

REM Open dashboard
start dashboard.html
```

## 📊 Understanding the Output

### Status Indicators
- **✓ COVERED** (Green): >70% of lecture keywords found in chapters
- **◐ PARTIAL** (Orange): 10-70% of keywords found (needs expansion)
- **○ PENDING** (Red): <10% or no keywords found (needs to be written)

### Console Output Example
```
================================================================================
TOPIC TRACKING SUMMARY
================================================================================

Statistics: 3 covered, 1 partial, 0 pending
Total lectures: 5

COVERED TOPICS:
✓ Lezione 1 (Mer 04/03/2026) - CECILIA PAGLIANTINI
✓ Lezione 3 (Mer 18/03/2026) - LUCA HELTAI
✓ Lezione 5 (Mer 01/04/2026) - LUCA HELTAI

PARTIAL TOPICS (partially covered):
◐ Lezione 2 (Mer 11/03/2026) - LUCA HELTAI

PENDING TOPICS (not yet covered):
○ Lezione 4 (Mer 25/03/2026) - LUCA HELTAI
```

### JSON Output (`topic_status.json`)
```json
{
  "summary": {
    "total": 5,
    "covered": 3,
    "partial": 1,
    "pending": 1
  },
  "topics": [
    {
      "lecture": 1,
      "date": "Mer 04/03/2026",
      "lecturer": "CECILIA PAGLIANTINI",
      "status": "COVERED",
      "content_preview": "Fondamenti della matematica numerica..."
    },
    ...
  ]
}
```

## 🔍 How It Works

### Step 1: Extract Lecture Topics
```
registro.txt
  ↓
Parser identifies:
  - Lecture number & date
  - Lecturer name
  - Topic content with technical terms
  ↓
Creates Topic objects with keywords
```

### Step 2: Analyze Chapters
```
Chapters/
  ↓
Scanner reads all .tex files
  ↓
Extracts section/subsection titles
  ↓
Builds keyword database for each chapter
```

### Step 3: Match & Score
```
For each lecture:
  - Extract keywords
  - Compare with chapter keywords
  - Calculate coverage percentage
  - Assign status (✓ / ◐ / ○)
```

### Step 4: Generate Reports
```
Create:
  - Console summary
  - JSON data file
  - HTML dashboard
```

## 📈 Your Topics at a Glance

| Lecture | Date | Topic | Coverage |
|---------|------|-------|----------|
| 1 | 04/03 | Fondamenti matematica numerica | ✓ Covered |
| 2 | 11/03 | Floating point & condizionamento | ◐ Partial |
| 3 | 18/03 | Sistemi lineari (metodi diretti) | ✓ Covered |
| 4 | 25/03 | Fattorizzazione QR | ○ Pending |
| 5 | 01/04 | Metodi iterativi | ✓ Covered |

## 🎨 Dashboard Features

The HTML dashboard provides:
- **Progress visualization** with animated progress bar
- **Color-coded sections** (green for done, orange for partial, red for pending)
- **Responsive design** (works on desktop, tablet, mobile)
- **Quick statistics** showing coverage at a glance
- **Detailed topic cards** with date, lecturer, and content preview
- **Sort by status** to prioritize work

Click "Refresh" in your browser (F5) to update after re-running the tracker.

## 📝 Workflow Recommendations

### Daily Workflow
1. After a new lecture, add it to `registro.txt`
2. When you write new content, add sections to your chapters
3. Run `track_all.bat` to see updated coverage

### Weekly Review
1. Check dashboard for any pending topics
2. Prioritize topics with partial coverage
3. Plan next week's writing based on pending items

### Before Submission
1. Run tracker to ensure all lectures are at least partially covered
2. Expand partial topics to full coverage if needed
3. Verify JSON export for final statistics

## 🔧 Customization

### Adjust Coverage Threshold
Edit `topic_tracker.py`, find line in `update_topic_status()`:
```python
if len(covered_keywords) > len(topic_keywords) * 0.7:  # Change 0.7 to desired threshold
```

### Add More Stopwords
In `extract_keywords()` method:
```python
stopwords = {'di', 'del', 'della', 'da', 'le', 'e', 'o', 'per', 'a', 'al', 'alla', 'in', 'il', 'uno', 'una'}
# Add more Italian words that should be ignored
```

### Change Output Formats
Modify the `print_summary()` and `export_json()` methods to customize output

## ⚙️ System Requirements

- **Python 3.6+** (3.8+ recommended)
- **Windows** (for batch scripts)
- Read access to `registro.txt` and `Chapters/` directory
- Text editor or browser to view outputs

## 🐛 Troubleshooting

### "Python is not recognized"
- Install Python from https://www.python.org
- During installation, check "Add Python to PATH"

### Empty tracking results
- Verify `registro.txt` contains lectures in expected format
- Check that chapter files have section headers with `\section{}` or `\subsection{}`
- Ensure file encoding is UTF-8

### Dashboard not opening
- Make sure `topic_status.json` exists
- Try opening `dashboard.html` manually with your browser
- Check browser console for any errors

### Incorrect coverage detection
- The system does keyword matching; if topics use different terminology, it may miss matches
- Check the `content_preview` in JSON to verify topic content
- Consider adding synonyms or expanding section titles in chapters

## 📋 File Structure

```
Appunti di calcolo.worktrees/
├── registro.txt                 (Your lecture log)
├── main.tex                     (Main LaTeX file)
├── Chapters/
│   ├── ch01/
│   │   └── chapter01.tex
│   ├── ch02/
│   │   └── chapter02.tex
│   └── appendice/
├── topic_tracker.py             (★ Main analyzer)
├── generate_dashboard.py         (★ Dashboard creator)
├── track_all.bat                (★ One-click execution)
├── run_tracker.bat              (Simple runner)
├── topic_status.json            (Generated data)
├── dashboard.html               (Generated visual report)
└── TRACKER_SETUP.md             (Extended documentation)
```

## 🚀 Future Enhancements

Possible improvements:
- [ ] Web interface for real-time tracking
- [ ] Git integration to track changes per commit
- [ ] LaTeX compilation integration
- [ ] Email notifications for pending topics
- [ ] Timeline visualization
- [ ] Export to Markdown/PDF
- [ ] Fuzzy string matching for better accuracy
- [ ] Multi-language support

## 📄 License & Usage

This topic tracking system is provided as part of your course notes organization. Feel free to modify and extend it for your needs.

## 💡 Tips

1. **Keep registro.txt updated**: Add lectures immediately after class
2. **Use clear section titles**: The more specific your chapter sections, the better the matching
3. **Review pending topics regularly**: Run the tracker weekly to stay on top of your progress
4. **Export JSON for backup**: Keep `topic_status.json` files as historical records of your progress

## 📞 Questions?

Refer to:
- **TRACKER_SETUP.md** for detailed technical documentation
- **Console output** when running the tracker for immediate feedback
- **HTML Dashboard** for visual representation of your progress

---

**Version**: 1.0  
**Last Updated**: 2026-04-20  
**Created for**: Calcolo Numerico Course Notes  
**Status**: ✓ Ready to Use

Happy note-taking! 📖
