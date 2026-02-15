"""
timeline.py - ציר זמן ויזואלי
צוות 2, זוג A

ראו docs/api_contract.md לפורמט הקלט והפלט.
"""

def create_timeline(images_data):
    # סינון ומיון לפי תאריך
    dated_images = [img for img in images_data if img.get("datetime")]
    dated_images.sort(key=lambda x: x["datetime"])

    colors = ["Tomato", "Orange", "DodgerBlue", "MediumSeaGreen", "Gray", "SlateBlue", "Violet", "LightGray"]

    # מיכל ראשי
    html = '<div style="position:relative; max-width: 1200px; margin: 50px auto; font-family: Arial, sans-serif;">'

    # קו מרכזי כחול
    html += '<div style="position:absolute; left:50%; width:8px; height:100%; background:#0000ff; transform: translateX(-50%); z-index: 1;"></div>'

    for i, img in enumerate(dated_images):
        side = "left" if i % 2 == 0 else "right"
        bg_color = colors[i % len(colors)]

        full_path = img.get("filename", "unknown")
        clean_name = os.path.basename(full_path).split('.')[0]

        # עיצוב יישור התיבה
        alignment_style = "margin-right: 55%; text-align: right;" if side == "left" else "margin-left: 55%; text-align: left;"

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

                <div class="name-wrapper" style="display: inline-block; cursor: pointer; position: relative; margin: 10px 0;">
                    <strong style="color: yellow; font-size: 1.6em;">{clean_name}</strong>

                    <img src="{full_path}" class="hover-image" style="
                        display: none; 
                        position: absolute; 
                        top: 110%; 
                        left: 50%; 
                        transform: translateX(-50%); 
                        width: 450px; 
                        z-index: 100; 
                        border: 6px solid white; 
                        border-radius: 15px;
                        box-shadow: 0 15px 40px rgba(0,0,0,0.6);">
                </div>

                <br>
                <small style="opacity: 0.8; font-size: 1em;">{img.get("camera_model", "Unknown Device")}</small>
            </div>
        </div>
        '''

    html += '</div>'

    # לוגיקת ה-CSS המשופרת
    css_logic = """
    <style>
        /* הצגת התמונה ב-Hover */
        .name-wrapper:hover .hover-image { 
            display: block !important; 
        }

        /* הדגשת שם התמונה */
        .name-wrapper:hover strong { 
            text-decoration: underline;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        /* הגדלת כל התיבה כשעומדים עליה */
        .timeline-item:hover .content-box {
            transform: scale(1.05); /* הגדלה של 5% */
            z-index: 10;
        }

        /* הגדלת הנקודה ב-Hover */
        .timeline-item:hover .timeline-dot { 
            background-color: yellow !important; 
            transform: translateX(-50%) scale(1.4);
            box-shadow: 0 0 10px yellow;
        }
    </style>
    """
    return css_logic + html
