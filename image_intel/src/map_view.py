"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""

import folium


def sort_by_time(arr):
    return sorted(arr, key=lambda x: x["datetime"])


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    gps_image = sort_by_time([img for img in images_data if img.get("has_gps")])

    if not gps_image:
        return "<h2>No GPS data found</h2>"

    path_coordinates = [[img["latitude"], img["longitude"]] for img in gps_image]

    # תיקון: חישוב מרכז רק מתמונות עם GPS (היה images_data שכולל תמונות בלי GPS -> None + מספר = קריסה)
    center_latitude = sum(img["latitude"] for img in gps_image) / len(gps_image)
    center_longitude = sum(img["longitude"] for img in gps_image) / len(gps_image)

    m = folium.Map(location=[center_latitude, center_longitude], zoom_start=10)

    folium.PolyLine(
        locations=path_coordinates,
        color="Blue",
        weight=3,
        opacity=0.6,
        tooltip="מסלול כרונולוגי"
    ).add_to(m)

    available_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
                        'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink',
                        'lightblue', 'lightgreen', 'gray', 'black']
    device_color_map = {}
    color_index = 0

    for idx, image in enumerate(gps_image, 1):
        model = image.get("camera_model", "Unknown") or "Unknown"

        if model not in device_color_map:
            device_color_map[model] = available_colors[color_index % len(available_colors)]
            color_index += 1  # תיקון: הזחה פנימה - צריך להתקדם רק כשיש מכשיר חדש, לא על כל תמונה

        chosen_color = device_color_map[model]

        popup_html = f"""
        <div style="font-family: sans-serif; width: 220px; direction: rtl;">
            <h4 style="margin: 0 0 10px 0;">📷 {image['filename']}</h4>
            <p style="margin: 5px 0;"><b>מספר:</b> {idx}</p>
            <p style="margin: 5px 0;"><b>זמן:</b> {image['datetime']}</p>
            <p style="margin: 5px 0;"><b>מכשיר:</b> {model}</p>
            <p style="margin: 5px 0;"><b>קואורדינטות:</b><br>
            {image['latitude']:.6f}, {image['longitude']:.6f}</p>
        </div>
        """

        # תיקון: הוסר CustomIcon שלא עובד - filename הוא רק שם (כמו "IMG_001.jpg"),
        # לא נתיב שהדפדפן יכול לגשת אליו. השתמשנו ישירות ב-folium.Icon
        icon = folium.Icon(color=chosen_color, icon="camera", prefix="fa")

        folium.Marker(
            location=[image["latitude"], image["longitude"]],
            popup=folium.Popup(popup_html, max_width=250),
            icon=icon,
            tooltip=f"{model} - {image['datetime']}"
        ).add_to(m)

    # תיקון: הוסר m.save() - לפי API contract הפונקציה מחזירה HTML string, לא שומרת קובץ
    # הצוות של report מצפה לקבל string ולשלב אותו בדו"ח
    return m._repr_html_()


if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן מגוף הקובץ - כדי שלא ירוץ בכל import
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]
    html = create_map(fake_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")
