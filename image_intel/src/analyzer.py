from geopy.distance import geodesic

fake_data = [
    {
        "filename": "test1.jpg",
        "datetime": "2025-01-12 08:30:00",
        "latitude": 32.0853,
        "longitude": 34.7818,
        "camera_make": "Samsung",
        "camera_model": "Galaxy S23",
        "has_gps": True
    },
    {
        "filename": "test2.jpg",
        "datetime": "2025-01-13 09:00:00",
        "latitude": 31.7683,
        "longitude": 35.2137,
        "camera_make": "Apple",
        "camera_model": "iPhone 15 Pro",
        "has_gps": True
    },
    {
        "filename": "test3.jpg",
        "datetime": None,
        "latitude": None,
        "longitude": None,
        "camera_make": None,
        "camera_model": None,
        "has_gps": False
    },
    {
        "filename": "test4.jpg",
        "datetime": "2025-01-13 14:12:45",
        "latitude": 31.7683,
        "longitude": 35.2137,
        "camera_make": "Apple",
        "camera_model": "iPhone 15",
        "has_gps": True
    },
    {
        "filename": "test5.jpg",
        "datetime": "2025-01-14 19:05:10",
        "latitude": 32.7940,
        "longitude": 34.9896,
        "camera_make": "Xiaomi",
        "camera_model": "Mi 13",
        "has_gps": True
    },
    {
        "filename": "test6.jpg",
        "datetime": "2025-01-15 07:45:22",
        "latitude": 29.5577,
        "longitude": 34.9519,
        "camera_make": "Canon",
        "camera_model": "EOS R6",
        "has_gps": True
    },
    {
        "filename": "test7.jpg",
        "datetime": "2025-01-16 22:18:03",
        "latitude": 32.3215,
        "longitude": 34.8532,
        "camera_make": "Nikon",
        "camera_model": "D750",
        "has_gps": True
    },
    {
        "filename": "test8.jpg",
        "datetime": "2025-01-17 11:02:37",
        "latitude": 31.0461,
        "longitude": 34.8516,
        "camera_make": "Sony",
        "camera_model": "Alpha A7 IV",
        "has_gps": True
    },
    {
        "filename": "test9.jpg",
        "datetime": "2025-01-18 16:29:54",
        "latitude": 33.0156,
        "longitude": 35.2700,
        "camera_make": "Samsung",
        "camera_model": "Galaxy S22",
        "has_gps": True
    },
    {
        "filename": "test10.jpg",
        "datetime": "2025-01-19 09:41:18",
        "latitude": 32.1093,
        "longitude": 34.8555,
        "camera_make": "Apple",
        "camera_model": "iPhone 14 Pro",
        "has_gps": True
    }

]

def sorted_dict(images_data):
    sorted_images = sorted(
        [img for img in images_data if img["datetime"]],
        key=lambda x: x["datetime"])
    return sorted_images

def detect_camera_switches(sorted_images):
    """
    מחזיר רשימה מסודרת של התמונות לפי הזמן שצולם
    :param images_data:
    :return:
    """

    switches = []
    for i in range(1, len(sorted_images)):
        prev_cam = sorted_images[i-1].get("camera_model")
        curr_cam = sorted_images[i].get("camera_model")
        if prev_cam and curr_cam and prev_cam != curr_cam:
            switches.append({
                "date": sorted_images[i]["datetime"],
                "from": prev_cam,
                "to": curr_cam
            })
    return switches

"""
analyzer.py - ניתוח דפוסים וזיהוי קשרים
צוות 2, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.
"""


def analyze(images_data):
    """
    מנתח את הנתונים ומוצא דפוסים.
    
    Args:
        images_data: רשימת מילונים מ-extract_all
    
    Returns:
        dict עם: total_images, images_with_gps, unique_cameras,
              date_range, insights
    """
    dict_result = {
        "total_images": 0,
        "images_with_gps": 0,
        "unique_cameras": 0,
        "date_range": 0,
    }
    count_gps = 0
    cameras = set()



    for image in images_data:
        if image["has_gps"]:
            count_gps += 1
        if image.get("camera_model"):
            cameras.add(image["camera_model"])
    dict_result["total_images"] = len(images_data)
    dict_result["images_with_gps"] = count_gps
    dict_result["unique_cameras"] = cameras
    dict_result["date_range"] = [images_data[0]["datetime"],images_data[-1]["datetime"]]

    return dict_result

# def cities(images_data):
#     address = []
#     geolocator = Nominatim(user_agent="geo_example")
#     for image in images_data:
#         latitude = image.get("latitude")
#         longitude = image.get("longitude")
#         if latitude and longitude:
#             location =  geolocator.reverse((latitude, longitude), language='he')
#             adrr = location.row['address']
#             address.append(adrr)
#     return address
# print(cities(sorted_dict(fake_data)))

from geopy.geocoders import Nominatim

def distance(image_data):
    distance_list = []
    for i in range(len(image_data)):
        if image_data[i].get("latitude") and image_data[i].get("longitude"):
            for j in range(len(image_data)):
                if i == j:
                    continue
                place = [image_data[i]["filename"]]
                if image_data[j].get("latitude") and image_data[j].get("longitude"):
                    point1 = image_data[i]["latitude"],image_data[i]["longitude"]
                    point2 = image_data[j]["latitude"],image_data[j]["longitude"]
                    if geodesic(point1, point2).kilometers < 1:
                        distance_list.append(image_data[j]["filename"])
        if len(place) > 1 and place not in distance_list:
            distance_list.append(place)
    return distance_list

print(distance(fake_data))
