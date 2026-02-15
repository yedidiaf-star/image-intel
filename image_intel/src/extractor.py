from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

=== תיקונים ===
1. has_gps מחזיר False במקום None - כדי שכל הצוותים יוכלו לעשות if/else כרגיל
2. הוספת טיפול במקרה שאין EXIF בתמונה (exif is None) - בלי זה הכל נופל על תמונה אחת בלי metadata
3. הסרת print(data) שהדפיס את כל ה-EXIF הגולמי לקונסול
4. הסרת files = os.listdir(path) שלא היה בשימוש
"""


def has_gps(data: dict):
    if "GPSInfo" in data:
        gps = data["GPSInfo"]
        if isinstance(gps, dict) and 2 in gps and 4 in gps:
            return True
    return False


def latitude(data: dict):
    try:
        if has_gps(data):
            n = data["GPSInfo"][2]
            return float(n[0]) + float(n[1] / 60) + float(n[2] / 3600)
    except (KeyError, TypeError, IndexError, ZeroDivisionError):
        pass
    return None


def longitude(data: dict):
    try:
        if has_gps(data):
            e = data["GPSInfo"][4]
            return float(e[0]) + float(e[1] / 60) + float(e[2] / 3600)
    except (KeyError, TypeError, IndexError, ZeroDivisionError):
        pass
    return None


def datatime(data: dict):
    try:
        return data["DateTimeOriginal"]
    except Exception:
        return None


def camera_make(data: dict):
    try:
        return data["Make"]
    except Exception:
        return None


def camera_model(data: dict):
    try:
        return data["Model"]
    except Exception:
        return None


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
              camera_make, camera_model, has_gps
    """
    path = Path(image_path)

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """
    path = Path(folder_path)
    images = {".jpg", ".jpeg", ".png", ".webp"}
    exif_list = []  # תיקון: שם משתנה - היה eixf_list (שגיאת כתיב)
    # תיקון: הוסר files = os.listdir(path) שלא היה בשימוש
    for file in sorted(path.glob('*')):  # תיקון: sorted כדי לקבל סדר קבוע
        if file.suffix.lower() in images:
            exif_list.append(extract_metadata(file))  # תיקון: היה Path(path / file) - מיותר, file כבר מלא
    return exif_list
