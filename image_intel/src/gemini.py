import folium


def sort_by_time(arr):
    # מיון לפי מחרוזת הזמן עובד מצוין בפורמט ISO (YYYY-MM-DD)
    return sorted(arr, key=lambda x: x["datetime"])


def create_map(images_data):
    # 1. סינון ומיון
    gps_images = sort_by_time([img for img in images_data if img["has_gps"]])

    if not gps_images:
        return "<h2>No GPS data found</h2>"

    # 2. הכנת רשימת הקואורדינטות לקו
    path_coordinates = [[img["latitude"], img["longitude"]] for img in gps_images]

    # 3. חישוב מרכז המפה
    avg_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    avg_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

    # 4. הוספת הקו המחבר (PolyLine) - פעם אחת מחוץ ללולאה
    folium.PolyLine(
        locations=path_coordinates,
        color="Black",
        weight=4,
        opacity=0.7,
        tooltip="מסלול כרונולוגי"
    ).add_to(m)

    # 5. הוספת סמנים
    for image in gps_images:
        # יצירת חלון קופץ (Popup) עם טקסט ותמונה מוגדלת
        html = f"""
            <div style="font-family: sans-serif; width: 200px;">
                <h4>{image['filename']}</h4>
                <p><b>Time:</b> {image['datetime']}</p>
                <p><b>Device:</b> {image['camera_model']}</p>
                <img src="{image['filename']}" width="180px" style="border-radius: 5px;">
            </div>
        """

        # אפשרות א': הצגת התמונה עצמה בתור האייקון על המפה
        try:
            icon = folium.CustomIcon(
                image["filename"],
                icon_size=(45, 45)
            )
        except:
            # גיבוי למקרה שהקובץ לא נמצא
            icon = folium.Icon(color="red", icon="info-sign")

        folium.Marker(
            location=[image["latitude"], image["longitude"]],
            popup=folium.Popup(html, max_width=250),
            icon=icon
        ).add_to(m)

    output_file = "my_photos_map.html"
    m.save(output_file)
    return output_file


# הרצה לבדיקה
fake_data = [
    {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
     "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
     "datetime": "2025-01-12 08:30:00"},
    {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
     "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
     "datetime": "2025-01-13 09:00:00"},
]

print(create_map(fake_data))