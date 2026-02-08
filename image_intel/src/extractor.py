"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.
"""

import os


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.
    
    Args:
        image_path: נתיב לקובץ תמונה
    
    Returns:
        dict עם: filename, datetime, latitude, longitude, 
              camera_make, camera_model, has_gps
    """
    pass


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.
    
    Args:
        folder_path: נתיב לתיקייה
    
    Returns:
        list של dicts (כמו extract_metadata)
    """
    pass
