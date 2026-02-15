"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B
"""

import folium
from typing import List, Dict


def sort_by_time(arr: List[Dict]) -> List[Dict]:
    """ממיין תמונות לפי זמן"""
    return sorted(arr, key=lambda x: x.get("datetime", ""))


def create_map(images_data: List[Dict], zoom_start: int = 10) -> str:
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all
        zoom_start: רמת זום התחלתית

    Returns:
        string של HTML (המפה)
    """
    if not images_data:
        return "<h2>No images provided</h2>"

    # סינון ומיון תמונות עם GPS
    gps_images = sort_by_time([img for img in images_data if img.get("has_gps")])

    if not gps_images:
        return "<h2>No GPS data found</h2>"

    # חישוב מרכז המפה
    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    # יצירת המפה
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)

    # הוספת מסלול כרונולוגי
    path_coordinates = [[img["latitude"], img["longitude"]] for img in gps_images]
    folium.PolyLine(
        locations=path_coordinates,
        color="black",
        weight=3,
        opacity=0.6,
        tooltip="מסלול כרונולוגי"
    ).add_to(m)

    # צבעים זמינים
    available_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
                        'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
                        'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', 'black']

    device_color_map = {}
    color_index = 0

    # הוספת סמנים
    for idx, image in enumerate(gps_images, 1):
        model = image.get("camera_model", "Unknown")

        # הקצאת צבע למכשיר
        if model not in device_color_map:
            device_color_map[model] = available_colors[color_index % len(available_colors)]
            color_index += 1

        chosen_color = device_color_map[model]

        # יצירת popup
        popup_html = f"""
            <div style="font-family: sans-serif; width: 220px;">
                <h4 style="margin: 0 0 10px 0;">📷 {image['filename']}</h4>
                <p style="margin: 5px 0;"><b>Photo #:</b> {idx}</p>
                <p style="margin: 5px 0;"><b>Time:</b> {image['datetime']}</p>
                <p style="margin: 5px 0;"><b>Device:</b> {model}</p>
                <p style="margin: 5px 0;"><b>Coordinates:</b><br>
                   {image['latitude']:.6f}, {image['longitude']:.6f}</p>
            </div>
        """

        icon = folium.Icon(color=chosen_color, icon="camera", prefix="fa")

        folium.Marker(
            location=[image["latitude"], image["longitude"]],
            popup=folium.Popup(popup_html, max_width=250),
            icon=icon,
            tooltip=f"{model} - {image['datetime']}"
        ).add_to(m)

    # שמירת הקובץ
    output_file = "my_photos_map.html"
    m.save(output_file)

    return m._repr_html_()


# Test
if __name__ == "__main__":
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]

    print("Creating map...")
    html_output = create_map(fake_data)
    print("Map saved to my_photos_map.html")
