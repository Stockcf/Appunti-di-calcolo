#!/usr/bin/env python3
"""
Generate an interactive HTML dashboard for topic tracking
"""

import json
import re
from pathlib import Path
from datetime import datetime


def generate_html_dashboard(topic_status_json: str = "topic_status.json") -> str:
    """Generate an HTML dashboard from topic status JSON"""
    
    json_path = Path(topic_status_json)
    
    if not json_path.exists():
        # Generate basic template if no data yet
        data = {
            "summary": {"total": 0, "covered": 0, "partial": 0, "pending": 0},
            "topics": []
        }
    else:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    summary = data.get("summary", {})
    topics = data.get("topics", [])
    
    # Group topics by status
    covered_topics = [t for t in topics if t.get("status") == "COVERED"]
    partial_topics = [t for t in topics if t.get("status") == "PARTIAL"]
    pending_topics = [t for t in topics if t.get("status") == "PENDING"]
    
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calcolo Numerico - Topic Tracker</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        header h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        
        header p {{
            color: #666;
            font-size: 14px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-card .number {{
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-card.covered .number {{ color: #10b981; }}
        .stat-card.partial .number {{ color: #f59e0b; }}
        .stat-card.pending .number {{ color: #ef4444; }}
        
        .stat-card .label {{
            font-size: 14px;
            color: #666;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }}
        
        .topic-section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .topic-section h2 {{
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .topic-section.covered h2 {{ color: #10b981; }}
        .topic-section.partial h2 {{ color: #f59e0b; }}
        .topic-section.pending h2 {{ color: #ef4444; }}
        
        .topic-list {{
            display: grid;
            gap: 15px;
        }}
        
        .topic-item {{
            padding: 15px;
            background: #f9fafb;
            border-left: 4px solid #e5e7eb;
            border-radius: 4px;
            transition: all 0.3s ease;
        }}
        
        .topic-item:hover {{
            transform: translateX(5px);
            background: #f3f4f6;
        }}
        
        .topic-item.covered {{
            border-left-color: #10b981;
        }}
        
        .topic-item.partial {{
            border-left-color: #f59e0b;
        }}
        
        .topic-item.pending {{
            border-left-color: #ef4444;
        }}
        
        .topic-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 8px;
        }}
        
        .topic-title {{
            font-weight: 600;
            color: #333;
        }}
        
        .topic-meta {{
            font-size: 12px;
            color: #999;
            margin-bottom: 8px;
        }}
        
        .topic-content {{
            font-size: 13px;
            color: #666;
            line-height: 1.5;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }}
        
        .badge.covered {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .badge.partial {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .badge.pending {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .empty {{
            text-align: center;
            padding: 40px;
            color: #999;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin: 15px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #10b981, #34d399);
            transition: width 0.3s ease;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
            font-size: 12px;
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: 1fr;
            }}
            
            header {{
                padding: 20px;
            }}
            
            .topic-section {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Calcolo Numerico - Topic Tracker</h1>
            <p>Tracking coverage of lecture topics in your written notes</p>
            
            <div class="progress-bar">
                <div class="progress-fill" style="width: {int((summary.get('covered', 0) / max(1, summary.get('total', 1))) * 100)}%"></div>
            </div>
            <p style="font-size: 12px; color: #666; margin-top: 8px;">
                {summary.get('covered', 0)} di {summary.get('total', 0)} argomenti completati
            </p>
        </header>
        
        <div class="stats">
            <div class="stat-card covered">
                <div class="label">Covered</div>
                <div class="number">{summary.get('covered', 0)}</div>
                <div class="label">✓ Complete</div>
            </div>
            <div class="stat-card partial">
                <div class="label">Partial</div>
                <div class="number">{summary.get('partial', 0)}</div>
                <div class="label">◐ In Progress</div>
            </div>
            <div class="stat-card pending">
                <div class="label">Pending</div>
                <div class="number">{summary.get('pending', 0)}</div>
                <div class="label">○ To Do</div>
            </div>
        </div>
        
        <div class="content">
            <!-- COVERED TOPICS -->
            <div class="topic-section covered">
                <h2>✓ Covered Topics ({len(covered_topics)})</h2>
                {'<div class="empty">No covered topics yet</div>' if not covered_topics else ''}
                <div class="topic-list">
    """
    
    for topic in covered_topics:
        html += f"""
                    <div class="topic-item covered">
                        <div class="topic-header">
                            <div class="topic-title">Lezione {topic.get('lecture', '?')}</div>
                            <span class="badge covered">COVERED</span>
                        </div>
                        <div class="topic-meta">
                            {topic.get('date', '')} • {topic.get('lecturer', '')}
                        </div>
                        <div class="topic-content">
                            {topic.get('content_preview', '')}
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </div>
            
            <!-- PARTIAL TOPICS -->
            <div class="topic-section partial">
                <h2>◐ Partial Topics ({})
    """.format(len(partial_topics))
    
    html += """</h2>
    """
    
    html += '                <div class="empty">No partial topics</div>' if not partial_topics else ''
    html += '                <div class="topic-list">'
    
    for topic in partial_topics:
        html += f"""
                    <div class="topic-item partial">
                        <div class="topic-header">
                            <div class="topic-title">Lezione {topic.get('lecture', '?')}</div>
                            <span class="badge partial">PARTIAL</span>
                        </div>
                        <div class="topic-meta">
                            {topic.get('date', '')} • {topic.get('lecturer', '')}
                        </div>
                        <div class="topic-content">
                            {topic.get('content_preview', '')}
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </div>
            
            <!-- PENDING TOPICS -->
            <div class="topic-section pending">
                <h2>○ Pending Topics ({})
    """.format(len(pending_topics))
    
    html += """</h2>
    """
    
    html += '                <div class="empty">No pending topics - all lectures covered!</div>' if not pending_topics else ''
    html += '                <div class="topic-list">'
    
    for topic in pending_topics:
        html += f"""
                    <div class="topic-item pending">
                        <div class="topic-header">
                            <div class="topic-title">Lezione {topic.get('lecture', '?')}</div>
                            <span class="badge pending">PENDING</span>
                        </div>
                        <div class="topic-meta">
                            {topic.get('date', '')} • {topic.get('lecturer', '')}
                        </div>
                        <div class="topic-content">
                            {topic.get('content_preview', '')}
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </div>
        </div>
        
        <footer>
            Generated on """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
            <br>
            Refresh your browser or re-run the tracker to update this dashboard
        </footer>
    </div>
</body>
</html>
    """
    
    return html


if __name__ == "__main__":
    import sys
    
    output_file = sys.argv[1] if len(sys.argv) > 1 else "dashboard.html"
    
    script_dir = Path(__file__).parent
    json_file = script_dir / "topic_status.json"
    
    html = generate_html_dashboard(str(json_file))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Dashboard generated: {output_file}")
