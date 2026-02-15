"""
report.py - הרכבת דו"ח HTML
צוות 3, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.
"""


from datetime import datetime


def create_report(images_data, map_html, timeline_html, analysis):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

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

    insights_html = ""
    for insight in analysis.get("insights", []):
        insights_html += f"<li>{insight}</li>"

    cameras_html = ""
    for cam in analysis.get("unique_cameras", []):
        cameras_html += f"<span class='badge'>{cam}</span> "

    html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>Image Intel Report</title>
        <style>
            /* עיצוב בסיסי ונקי */
            body {{ 
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 30px; 
                background: #f0f2f5; 
                color: #333;
                line-height: 1.6;
            }}

            /* כותרת הדוח */
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

            /* סקשנים */
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

            /* כרטיסי סטטיסטיקה */
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

            /* תגיות מכשירים */
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

            /* התאמה למפה וציר זמן */
            iframe, div.folium-map {{ border-radius: 8px; overflow: hidden; }}
        </style>
    </head>
    <body>
        <div class="header">
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

        <div style="text-align:center; color:#888; margin-top:30px; padding-bottom: 20px;">
            Image Intel | האקתון 2025
        </div>
    </body>
    </html>
    """
    return html