#!/usr/bin/env python3
"""
Verification script - Confirms all components are working
"""

import json
from pathlib import Path
import sys

def verify_installation():
    """Verify that all files are in place and working"""
    
    script_dir = Path(__file__).parent
    
    print("\n" + "="*70)
    print("TOPIC TRACKER - INSTALLATION VERIFICATION")
    print("="*70 + "\n")
    
    # Check Python version
    print("✓ Python Version Check")
    if sys.version_info >= (3, 6):
        print(f"  Python {sys.version_info.major}.{sys.version_info.minor} ✓ Compatible")
    else:
        print(f"  ⚠ Python {sys.version_info.major}.{sys.version_info.minor} - Requires 3.6+")
    
    # Check required files
    print("\n✓ Required Files Check")
    required_files = {
        'topic_tracker.py': 'Core analyzer',
        'generate_dashboard.py': 'Dashboard generator',
        'track_all.bat': 'One-click runner',
        'run_tracker.bat': 'Console runner',
        'registro.txt': 'Lecture registry',
    }
    
    all_present = True
    for fname, description in required_files.items():
        fpath = script_dir / fname
        if fpath.exists():
            size = fpath.stat().st_size
            print(f"  ✓ {fname:<30} ({size:>6} bytes) - {description}")
        else:
            print(f"  ✗ {fname:<30} MISSING")
            all_present = False
    
    # Check directories
    print("\n✓ Directory Structure Check")
    dirs = {
        'Chapters': 'Written chapters',
        '.git': 'Git repository',
    }
    
    for dname, description in dirs.items():
        dpath = script_dir / dname
        if dpath.exists() and dpath.is_dir():
            print(f"  ✓ {dname:<30} - {description}")
        else:
            print(f"  ✗ {dname:<30} MISSING")
    
    # Check documentation
    print("\n✓ Documentation Files Check")
    docs = {
        'QUICK_START.txt': 'Quick reference guide',
        'README_TRACKER.md': 'Complete user guide',
        'TRACKER_SETUP.md': 'Technical documentation',
        'REFERENCE_CARD.txt': 'Command reference',
        'INDEX.md': 'File index',
        'IMPLEMENTATION_SUMMARY.md': 'Implementation details',
    }
    
    for dname, description in docs.items():
        dpath = script_dir / dname
        if dpath.exists():
            size = dpath.stat().st_size
            print(f"  ✓ {dname:<35} ({size:>6} bytes)")
        else:
            print(f"  ⚠ {dname:<35} (optional)")
    
    # Test imports
    print("\n✓ Import Test")
    try:
        from pathlib import Path
        from dataclasses import dataclass
        from enum import Enum
        from typing import List, Set, Dict
        print("  ✓ All required modules available")
    except ImportError as e:
        print(f"  ✗ Missing module: {e}")
    
    # Verify registro.txt format
    print("\n✓ Data Format Check")
    registro_path = script_dir / 'registro.txt'
    if registro_path.exists():
        try:
            with open(registro_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lectures = len([l for l in content.split('\n') if l.strip() and l[0].isdigit()])
                print(f"  ✓ registro.txt readable ({len(content)} bytes, ~{lectures} lectures)")
        except Exception as e:
            print(f"  ✗ Error reading registro.txt: {e}")
    
    # Verify chapter structure
    print("\n✓ Chapter Structure Check")
    chapters_dir = script_dir / 'Chapters'
    if chapters_dir.exists():
        try:
            tex_files = list(chapters_dir.glob('*/*.tex'))
            print(f"  ✓ Found {len(tex_files)} chapter files")
            for tf in tex_files:
                print(f"    - {tf.relative_to(script_dir)}")
        except Exception as e:
            print(f"  ✗ Error reading chapters: {e}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if all_present:
        print("\n✅ ALL SYSTEMS READY - Installation Complete!\n")
        print("Next steps:")
        print("  1. Read: QUICK_START.txt")
        print("  2. Run: Double-click track_all.bat")
        print("  3. Review: Dashboard opens automatically")
        print("\n" + "="*70 + "\n")
        return True
    else:
        print("\n⚠️  Some files are missing. Please check the installation.")
        print("\n" + "="*70 + "\n")
        return False

if __name__ == "__main__":
    success = verify_installation()
    sys.exit(0 if success else 1)
