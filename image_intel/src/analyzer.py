"""
analyzer.py - ניתוח דפוסים וזיהוי קשרים
צוות 2, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. הוחלף geopy ב-haversine ידני - geopy לא ב-requirements.txt ומוסיף תלות מיותרת
2. insights מחזיר list של strings (לפי API contract) - היה dict בתוך dict
3. date_range מטפל ברשימה ריקה (אם אין תמונות עם datetime)
4. תיקון f-string עם מרכאות מקוננות (syntax error)
5. fake_data הועבר ל-if __name__
6. הוספת detect_camera_switches לתוך insights
7. הוספת זיהוי פערי זמן
"""

import math
from datetime import datetime


def haversine_km(lat1, lon1, lat2, lon2):
    """
    מחשב מרחק בק"מ בין שתי נקודות GPS.
    מחליף את geopy.distance.geodesic - אותה פונקציונליות, בלי תלות חיצונית.
    """
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def detect_camera_switches(sorted_images):
    """
    מזהה מתי הסוכן החליף מכשיר.
    """
    switches = []
    for i in range(1, len(sorted_images)):
        prev_cam = sorted_images[i - 1].get("camera_model")
        curr_cam = sorted_images[i].get("camera_model")
        if prev_cam and curr_cam and prev_cam != curr_cam:
            switches.append({
                "date": sorted_images[i]["datetime"],
                "from": prev_cam,
                "to": curr_cam
            })
    return switches


def find_nearby_images(image_data, threshold_km=1):
    """
    תיקון של distance() המקורי - אותה לוגיקה אבל עם haversine במקום geopy.
    מוצא קבוצות של תמונות שצולמו ברדיוס נתון.
    """
    distance_list = []
    for i in range(len(image_data)):
        if not (image_data[i].get("latitude") and image_data[i].get("longitude")):
            continue
        place = [image_data[i]["filename"]]
        for j in range(len(image_data)):
            if i == j:
                continue
            if not (image_data[j].get("latitude") and image_data[j].get("longitude")):
                continue
            dist = haversine_km(
                image_data[i]["latitude"], image_data[i]["longitude"],
                image_data[j]["latitude"], image_data[j]["longitude"]
            )
            if dist < threshold_km:
                place.append(image_data[j]["filename"])
        place.sort()
        if len(place) > 1 and place not in distance_list:
            distance_list.append(place)
    return distance_list


def detect_time_gaps(sorted_images, min_hours=6):
    """מזהה פערי זמן גדולים בין תמונות."""
    gaps = []
    for i in range(1, len(sorted_images)):
        try:
            t1 = datetime.strptime(sorted_images[i - 1]["datetime"][:19], "%Y:%m:%d %H:%M:%S")
            t2 = datetime.strptime(sorted_images[i]["datetime"][:19], "%Y:%m:%d %H:%M:%S")
        except ValueError:
            try:
                t1 = datetime.strptime(sorted_images[i - 1]["datetime"][:19], "%Y-%m-%d %H:%M:%S")
                t2 = datetime.strptime(sorted_images[i]["datetime"][:19], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
        diff_hours = (t2 - t1).total_seconds() / 3600
        if diff_hours >= min_hours:
            gaps.append({
                "from": sorted_images[i - 1]["datetime"],
                "to": sorted_images[i]["datetime"],
                "hours": round(diff_hours, 1)
            })
    return gaps


def analyze(images_data):
    """
    מנתח את הנתונים ומוצא דפוסים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        dict עם: total_images, images_with_gps, unique_cameras,
              date_range, insights
    """
    if not images_data:
        return {
            "total_images": 0,
            "images_with_gps": 0,
            "unique_cameras": [],
            "date_range": None,
            "insights": ["לא נמצאו תמונות לניתוח"]
        }

    # מיון לפי תאריך
    sorted_images = sorted(
        [img for img in images_data if img.get("datetime")],
        key=lambda x: x["datetime"]
    )

    # ספירות בסיסיות
    count_gps = 0
    cameras = set()

    for image in images_data:
        if image.get("has_gps"):
            count_gps += 1
        if image.get("camera_model"):
            cameras.add(image["camera_model"])

    # טווח תאריכים - תיקון: טיפול ברשימה ריקה
    date_range = None
    if sorted_images:
        date_range = {
            "start": sorted_images[0]["datetime"],
            "end": sorted_images[-1]["datetime"]
        }

    # תובנות - תיקון: insights הוא list של strings (לא dict בתוך dict)
    insights = []

    insights.append(f"נמצאו {len(images_data)} תמונות, מתוכן {count_gps} עם GPS")

    # מכשירים
    cameras_list = list(cameras)
    if len(cameras_list) > 1:
        # תיקון: f-string עם מרכאות מקוננות - היה syntax error
        insights.append(f"נמצאו {len(cameras_list)} מכשירים שונים: {', '.join(cameras_list)}")
    elif len(cameras_list) == 1:
        insights.append(f"כל התמונות צולמו עם מכשיר אחד: {cameras_list[0]}")

    # החלפות מכשיר
    if sorted_images:
        switches = detect_camera_switches(sorted_images)
        for sw in switches:
            insights.append(f"ב-{sw['date'][:10]} הסוכן עבר מ-{sw['from']} ל-{sw['to']}")

    # ריכוזים גיאוגרפיים
    nearby = find_nearby_images(images_data)
    for group in nearby:
        insights.append(f"תמונות שצולמו ברדיוס 1 ק\"מ: {', '.join(group)}")

    # פערי זמן
    if sorted_images:
        gaps = detect_time_gaps(sorted_images)
        for gap in gaps:
            insights.append(f"פער של {gap['hours']} שעות בין {gap['from'][:10]} ל-{gap['to'][:10]}")

    return {
        "total_images": len(images_data),
        "images_with_gps": count_gps,
        "unique_cameras": cameras_list,  # תיקון: היה set, צריך list
        "date_range": date_range,
        "insights": insights
    }


if __name__ == "__main__":
    # תיקון: fake_data הועבר לכאן - היה בגוף הקובץ ורץ בכל import
    fake_data = [
        {"filename": "test1.jpg", "datetime": "2025-01-12 08:30:00",
         "latitude": 32.0853, "longitude": 34.7818,
         "camera_make": "Samsung", "camera_model": "Galaxy S23", "has_gps": True},
        {"filename": "test2.jpg", "datetime": "2025-01-13 09:00:00",
         "latitude": 31.7683, "longitude": 35.2137,
         "camera_make": "Apple", "camera_model": "iPhone 15 Pro", "has_gps": True},
        {"filename": "test3.jpg", "datetime": None,
         "latitude": None, "longitude": None,
         "camera_make": None, "camera_model": None, "has_gps": False},
    ]
    result = analyze(fake_data)
    print(f"Total: {result['total_images']}")
    print(f"Cameras: {result['unique_cameras']}")
    print("\nInsights:")
    for insight in result['insights']:
        print(f"  - {insight}")
