from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.
"""
def has_gps(data:dict):
    if "GPSInfo" in data:
        if type(data["GPSInfo"]) == dict:
            return True
    return None
def latitude(data:dict):
    if has_gps(data) is not None:
        n = data["GPSInfo"][2]
        return float(n[0]) + float(n[1]/60) + float(n[2]/3600)
    return None

def longitude(data:dict):
    if has_gps(data) is not None:
        e = data["GPSInfo"][4]
        return float(e[0]) + float(e[1]/60) + float(e[2]/3600)
    return None
def datatime(data:dict):
    try:
        return data["DateTimeOriginal"]
    except Exception:
        return None

def camera_make(data:dict):
    try:
        return data["Make"]
    except Exception:
        return None


def camera_model(data:dict):
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
    img = Image.open(image_path)
    exif = img._getexif()
    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value
    print(data)
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
    eixf_list = []
    files = os.listdir(path)
    for file in path.glob('*'):
        if file.suffix.lower() in images:
            eixf_list.append(extract_metadata(Path(path / file)))
    return eixf_list

