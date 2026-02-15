"""
report.py - הרכבת דו"ח HTML
צוות 3, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. docstring הוזז לתחילת הפונקציה (היה אחרי now = ...)
2. הוספת רשימת תמונות עם פרטים (היה חסר)
3. הוספת טיפול ב-insights שהם לא strings (למקרה שצוות analyzer מחזיר פורמט לא צפוי)
"""

from datetime import datetime


def create_report(images_data, map_html, timeline_html, analysis):
    """
    מרכיב את כל החלקים לדו"ח HTML אחד.

    Args:
        images_data: רשימת מילונים מ-extract_all
        map_html: HTML של המפה מ-create_map
        timeline_html: HTML של ציר הזמן מ-create_timeline
        analysis: מילון התובנות מ-analyze

    Returns:
        string של HTML מלא (הדו"ח הסופי)
    """
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    # תיקון: הוספת str() על כל insight למקרה שהוא לא string
    insights_html = ""
    for insight in analysis.get("insights", []):
        insights_html += f"<li>{str(insight)}</li>"

    cameras_html = ""
    for cam in analysis.get("unique_cameras", []):
        cameras_html += f"<span class='badge'>{cam}</span> "

    # תיקון: הוספת רשימת תמונות
    images_list_html = ""
    for img in images_data:
        gps_badge = '<span style="background:#4ade80; color:#166534; padding:2px 8px; border-radius:10px; font-size:0.8em;">GPS</span>' if img.get("has_gps") else '<span style="background:#fca5a5; color:#991b1b; padding:2px 8px; border-radius:10px; font-size:0.8em;">ללא GPS</span>'
        camera = img.get("camera_model") or "לא ידוע"
        dt = img.get("datetime") or "לא ידוע"
        images_list_html += f"""
        <div style="display:flex; align-items:center; gap:12px; padding:10px; margin:5px 0; background:#fafafa; border-radius:8px;">
            <span style="font-size:1.5em;">📷</span>
            <div>
                <div style="font-weight:bold;">{img['filename']}</div>
                <div style="color:#666; font-size:0.85em;">{dt} | {camera} {gps_badge}</div>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>Image Intel Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px;
                background: #f0f2f5;
                color: #333;
                line-height: 1.6;
            }}
            .header {{
                background: linear-gradient(135deg, #1B4F72 0%, #2c3e50 100%);
                color: white;
                padding: 40px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                margin-bottom: 30px;
            }}
            .header h1 {{ margin: 0; font-size: 2.5em; }}
            .header p {{ opacity: 0.9; margin-top: 10px; }}
            .section {{
                background: white;
                padding: 25px;
                margin: 25px 0;
                border-radius: 10px;
                box-shadow: 0 2px 15px rgba(0,0,0,0.05);
                border: 1px solid #e1e4e8;
            }}
            .section h2 {{
                color: #1B4F72;
                border-bottom: 2px solid #f0f2f5;
                padding-bottom: 12px;
                margin-top: 0;
            }}
            .stats {{
                display: flex;
                gap: 20px;
                justify-content: center;
                margin-top: 15px;
            }}
            .stat-card {{
                background: #f8fbff;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                flex: 1;
                border: 1px solid #dbeafe;
            }}
            .stat-number {{
                font-size: 2.5em;
                font-weight: 800;
                color: #1B4F72;
                display: block;
                line-height: 1;
            }}
            .badge {{
                background: #2E86AB;
                color: white;
                padding: 6px 14px;
                border-radius: 20px;
                margin: 4px;
                display: inline-block;
                font-size: 0.9em;
                font-weight: 500;
                box-shadow: 0 2px 4px rgba(46, 134, 171, 0.2);
            }}
            ul {{ padding-right: 20px; }}
            li {{ margin-bottom: 8px; }}
            iframe, div.folium-map {{ border-radius: 8px; overflow: hidden; }}
            @media print {{
                button {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <p>בס״ד</p>
            <h1>Image Intel Report</h1>
            <p>נוצר ב-{now}</p>
        </div>

        <div class="section">
            <h2>סיכום</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('total_images', 0)}</div>
                    <div>תמונות</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('images_with_gps', 0)}</div>
                    <div>עם GPS</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(analysis.get('unique_cameras', []))}</div>
                    <div>מכשירים</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>תובנות מרכזיות</h2>
            <ul>{insights_html}</ul>
        </div>

        <div class="section">
            <h2>מפה</h2>
            {map_html}
        </div>

        <div class="section">
            <h2>ציר זמן</h2>
            {timeline_html}
        </div>

        <div class="section">
            <h2>מכשירים</h2>
            {cameras_html}
        </div>

        <div class="section">
            <h2>רשימת תמונות</h2>
            {images_list_html}
        </div>

        <button onclick="downloadPDF()" style="display:block; margin:20px auto; padding:12px 30px; background:#1B4F72; color:white; border:none; border-radius:8px; font-size:1em; cursor:pointer;">הורד כ-PDF</button>
        <script>
        function downloadPDF() {{
            window.print();
        }}
        </script>

        <div style="text-align:center; color:#888; margin-top:30px; padding-bottom: 20px;">
            Image Intel | האקתון 2025
        </div>
    </body>
    </html>
    """
    return html
