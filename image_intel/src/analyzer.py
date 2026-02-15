from geopy.geocoders import Nominatim

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
    count_im = 0
    count_gps = 0
    cameras = set()



    for image in images_data:
        count_im += 1
        if image["has_gps"]:
            count_gps += 1
        if image.get("camera_model"):
            cameras.add(image["camera_model"])
    dict_result["total_images"] = count_im
    dict_result["images_with_gps"] = count_gps
    dict_result["unique_cameras"] = cameras
    dict_result["date_range"] = [sorted_images[0]["datetime"],sorted_images[-1]["datetime"]]

    return dict_result

def citis()



print(analyze(fake_data))