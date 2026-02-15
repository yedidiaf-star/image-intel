"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.
"""

import folium

fake_data = [
    {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
     "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
     "datetime": "2025-01-12 08:30:00"},
    {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
     "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
     "datetime": "2025-01-13 09:00:00"},
]

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
    gps_image = sort_by_time([gps_image for gps_image in images_data if gps_image["has_gps"]])


    if not gps_image:
        return "<h2>No GPS data found</h2>"

    path_coordinates = [[img["latitude"], img["longitude"]] for img in gps_image]

    center_longitude = sum( img["longitude"] for img in images_data) / len(gps_image)
    center_latitude = sum(img["latitude"] for img in images_data)/ len(gps_image)

    m = folium.Map(location=[center_latitude, center_longitude], zoom_start=10)


    folium.PolyLine(
        locations=path_coordinates,
        color="Black",
        weight=3,
        opacity=0.6,
        tooltip="מסלול כרונולוגי"
    ).add_to(m)

    available_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue',
                        'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray',
                        'black', 'lightgray']

    device_color_map = {}
    color_index = 0


    for image in gps_image:
        model = image["camera_model"]

        if model not in device_color_map:
            device_color_map[model] = available_colors[color_index % len(available_colors)]
            color_index += 1

        chosen_color = device_color_map[model]

        html = f"""
                    <div style="font-family: sans-serif; width: 200px;">
                        <h4>{image['filename']}</h4>
                        <p><b>Time:</b> {image['datetime']}</p>
                        <p><b>Device:</b> {model}</p>
                        <img src="{image['filename']}" width="180px" style="border-radius: 5px;">
                    </div>
                """
        icon = folium.Icon(color=chosen_color, icon="camera", prefix="fa")

        folium.Marker(
            location=[image["latitude"], image["longitude"]],
            popup=folium.Popup(html, max_width=250),
            icon=icon,
            tooltip=f"Device: {model}"  # מציג את שם המכשיר בריחופ עם העכבר
        ).add_to(m)

        try:
            icon = folium.CustomIcon(
                image["filename"],
                icon_size=(45, 45)
            )
        except:
            icon = folium.Icon(color="red", icon="info-sign")

        folium.Marker(
            location=[image["latitude"], image["longitude"]],
            popup=folium.Popup(html, max_width=250),
            icon=icon
        ).add_to(m)



    output_file = "my_photos_map.html"
    m.save(output_file)
    return output_file
print(create_map(fake_data))