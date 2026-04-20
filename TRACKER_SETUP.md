# Topic Tracking System for Numerical Calculus Notes

## Overview
This system intelligently tracks which lecture topics from your class notes have been covered in your written documentation and which still need to be addressed.

## Files
- **`topic_tracker.py`**: Main Python script that analyzes your notes
- **`run_tracker.bat`**: Batch file to run the tracker (Windows)
- **`registro.txt`**: Source file with lecture topics (auto-detected)
- **`Chapters/`**: Directory with your written chapters (auto-detected)
- **`topic_status.json`**: Output file with tracking data (auto-generated)

## How It Works

### 1. Parsing Lecture Topics
The tracker reads `registro.txt` and extracts:
- Lecture number and date
- Lecturer name
- Topic content (keywords like "fattorizzazione LU", "metodi iterativi", etc.)

### 2. Analyzing Written Content
The tracker examines all `.tex` files in the `Chapters/` directory and extracts:
- Section and subsection titles
- Technical terminology mentioned in the chapters

### 3. Matching Topics to Chapters
For each lecture, the system:
- Extracts key terms from the lecture content
- Compares them with keywords found in your chapters
- Assigns a status based on coverage percentage:
  - **✓ COVERED**: >70% of key terms found in chapters
  - **◐ PARTIAL**: 1-70% of key terms found in chapters
  - **○ PENDING**: No or minimal coverage in chapters

## Usage

### Option 1: Using the Batch File (Windows)
Double-click `run_tracker.bat` to execute the tracker.

### Option 2: Using Command Line
```cmd
cd "C:\Users\ricca\Desktop\II anno\Calcolo numerico\Appunti di calcolo.worktrees\copilot-worktree-2026-04-20T10-07-37"
python topic_tracker.py
```

## Output

### Console Output
When you run the tracker, you'll see:
- Summary statistics (how many topics are covered/partial/pending)
- List of fully covered topics
- List of partially covered topics
- List of pending topics

Example:
```
================================================================================
TOPIC TRACKING SUMMARY
================================================================================

Statistics: 3 covered, 1 partial, 0 pending
Total lectures: 4

COVERED TOPICS:
✓ Lezione 3 (Mer 18/03/2026) - LUCA HELTAI
✓ Lezione 4 (Mer 25/03/2026) - LUCA HELTAI
...
```

### JSON Export
The script automatically exports detailed data to `topic_status.json` with:
- Summary statistics
- Individual topic information
- Content previews
- Detailed status for each lecture

## Interpreting the Status Symbols

- **✓** (Check mark): Topic is well-covered in your notes
- **◐** (Half circle): Topic is partially covered; you might want to expand it
- **○** (Circle): Topic hasn't been written yet; prioritize this

## Workflow Suggestion

1. **First Run**: Execute the tracker to get a baseline of what's covered
2. **Review Pending Topics**: Look at pending topics to decide what to write next
3. **Update Chapters**: Add content for pending or partial topics
4. **Re-run Tracker**: Execute again to verify your progress

## Example Topics from Your Lectures

### Lecture 1 (04/03/2026): Foundational Topics
- Fondamenti della matematica numerica
- Problema ben posto
- Stabilità e convergenza
- Norme matriciali

### Lecture 2 (11/03/2026): Floating Point
- Condizionamento
- Aritmetica floating point
- Cancellazione numerica

### Lecture 3 (18/03/2026): Linear Systems - Direct Methods
- Fattorizzazione LU
- Eliminazione di Gauss
- Metodo di sostituzione

### Lecture 4 (25/03/2026): QR Factorization
- Fattorizzazione QR
- Matrici di Householder
- Sistemi sovradeterminati

### Lecture 5 (01/04/2026): Iterative Methods
- Metodi iterativi
- Jacobi e Gauss-Seidel
- Convergenza

## Technical Details

### Keyword Extraction
The system uses regex patterns to identify:
- Capitalized technical terms (e.g., "Fattorizzazione LU")
- Section/subsection titles from LaTeX
- Italian stopwords are filtered out automatically

### Matching Algorithm
- Case-insensitive comparison
- Simple set intersection to find coverage overlap
- Configurable threshold (70% for COVERED status)

## Customization

If you want to modify the matching algorithm, you can edit `topic_tracker.py`:
- Change the `COVERED` threshold (currently 0.7) in the `update_topic_status()` method
- Add more stopwords in the `extract_keywords()` method
- Modify regex patterns for your specific needs

## Troubleshooting

### Script doesn't run
- Ensure Python 3.6+ is installed
- Check that `registro.txt` and `Chapters/` exist in the same directory
- Make sure you have read permissions for these files

### No output or empty results
- Verify `registro.txt` format matches the expected pattern
- Check that chapter files contain section headers with technical terms
- Try running with verbose output (you can add `print()` statements)

### Incorrect coverage detection
- The system looks for exact keyword matches
- If a topic uses different terminology than your chapters, it might show as pending
- You can manually verify by opening the chapters and checking content

## Future Enhancements

Potential improvements:
- Support for multiple languages (currently Italian-focused)
- Fuzzy matching for similar keywords
- Time-based filtering (e.g., "topics written this week")
- Integration with LaTeX compilation
- Web interface for easier visualization
- Export to Markdown or other formats

## Notes

- The tracker runs in read-only mode; it won't modify any files
- Running the tracker multiple times is safe
- The `topic_status.json` file is overwritten each time (consider backing it up if needed)
- Performance is typically <1 second for small projects

---
**Last Updated**: 2026-04-20
**Version**: 1.0
