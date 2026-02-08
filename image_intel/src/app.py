"""
app.py - Flask web server
צוות 3, זוג A

מחבר את כל המודולים לממשק ווב.
"""

from flask import Flask, render_template, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    """דף הבית"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_images():
    """מקבל נתיב תיקייה, מריץ את כל המודולים, מחזיר דו"ח"""
    folder_path = request.form.get('folder_path')
    
    if not folder_path or not os.path.isdir(folder_path):
        return "תיקייה לא נמצאה", 400
    
    # TODO: חברו את המודולים כאן
    # from extractor import extract_all
    # from map_view import create_map
    # from timeline import create_timeline
    # from analyzer import analyze
    # from report import create_report
    
    return "TODO: connect modules"


if __name__ == '__main__':
    app.run(debug=True)
