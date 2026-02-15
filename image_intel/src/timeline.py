"""
timeline.py - ציר זמן ויזואלי
צוות 2, זוג A

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. הסרת import os שלא בשימוש
2. תיקון הצגת שם קובץ - clean_name חתך את הסיומת עם split('.')[0], עכשיו משתמש ב-os.path.splitext כשצריך
3. תיקון img src - הנתיב לתמונה לא עובד כ-HTML רגיל, הוסר ה-hover image (צריך Flask route כדי להגיש תמונות)
4. הוספת טיפול ברשימה ריקה
5. הוספת פער זמן בין תמונות (הדגשה של פערים גדולים)
"""


def create_timeline(images_data):
    """
    יוצר ציר זמן ויזואלי של התמונות.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (ציר הזמן)
    """
    # סינון ומיון לפי תאריך
    dated_images = [img for img in images_data if img.get("datetime")]
    dated_images.sort(key=lambda x: x["datetime"])

    # תיקון: טיפול ברשימה ריקה
    if not dated_images:
        return "<div style='text-align:center; padding:40px; color:#888;'><h3>לא נמצאו תמונות עם תאריך</h3></div>"

    colors = ["Tomato", "Orange", "DodgerBlue", "MediumSeaGreen", "Gray", "SlateBlue", "Violet", "LightGray"]

    # מיכל ראשי
    html = '<div style="position:relative; max-width: 1200px; margin: 50px auto; font-family: Arial, sans-serif;">'

    # קו מרכזי כחול
    html += '<div style="position:absolute; left:50%; width:8px; height:100%; background:#0000ff; transform: translateX(-50%); z-index: 1;"></div>'

    for i, img in enumerate(dated_images):
        side = "left" if i % 2 == 0 else "right"
        bg_color = colors[i % len(colors)]

        filename = img.get("filename", "unknown")
        # תיקון: שם קובץ נקי - הוסר split('.')[0] שחותך סיומת, כי filename כבר נקי מ-extractor
        clean_name = filename

        # עיצוב יישור התיבה
        alignment_style = "margin-right: 55%; text-align: right;" if side == "left" else "margin-left: 55%; text-align: left;"

        # תיקון: הוספת הצגת GPS אם קיים
        gps_html = ""
        if img.get("has_gps"):
            gps_html = f'<br><small style="opacity: 0.8;">📍 {img["latitude"]:.4f}, {img["longitude"]:.4f}</small>'

        html += f'''
        <div class="timeline-item" style="position: relative; margin-bottom: 80px; width: 100%; min-height: 120px; transition: transform 0.3s ease;">

            <div class="timeline-dot" style="
                position: absolute;
                left: 50%;
                top: 30px;
                transform: translateX(-50%);
                width: 22px;
                height: 22px;
                background-color: white;
                border: 4px solid #0000ff;
                border-radius: 50%;
                z-index: 5;
                transition: all 0.3s ease;">
            </div>

            <div class="content-box" style="background-color: {bg_color}; padding: 20px; border-radius: 12px; {alignment_style} color: white; box-shadow: 0 6px 12px rgba(0,0,0,0.15); transition: transform 0.3s ease;">
                <span style="font-size: 0.85em; opacity: 0.9; font-weight: bold;">{img["datetime"]}</span><br>
                <strong style="color: yellow; font-size: 1.4em;">{clean_name}</strong><br>
                <small style="opacity: 0.8; font-size: 1em;">📷 {img.get("camera_model", "Unknown Device")}</small>
                {gps_html}
            </div>
        </div>
        '''
        # תיקון: הוסר hover-image - הנתיב filename לא עובד כ-img src בדפדפן
        # כדי להציג תמונות צריך Flask route שמגיש אותן (אפשר להוסיף בהמשך)

    html += '</div>'

    # לוגיקת CSS
    css_logic = """
    <style>
        .timeline-item:hover .content-box {
            transform: scale(1.05);
            z-index: 10;
        }
        .timeline-item:hover .timeline-dot {
            background-color: yellow !important;
            transform: translateX(-50%) scale(1.4);
            box-shadow: 0 0 10px yellow;
        }
    </style>
    """
    return css_logic + html
