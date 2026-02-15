"""
app.py - Flask web server
צוות 3, זוג A

=== תיקונים ===
1. הסרת import כפול (from map_view import create_map הופיע פעמיים)
2. הסרת @app.route('/') כפול
3. הסרת קריאות כפולות ב-analyze_images (extract/map/timeline/analyze רצו פעמיים)
4. הסרת print(len(images_data)) מתוך ה-route
5. הסרת פונקציות fake שלא בשימוש
6. הוספת טיפול שגיאות ורשימה ריקה
"""

from extractor import extract_all
from report import create_report
from map_view import create_map
from analyzer import analyze
from timeline import create_timeline
from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='templates')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'images', 'uploads')


# תיקון: הוסר @app.route('/') כפול
@app.route('/')
def index():
    """דף הבית - מנקה קבצים ישנים"""
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"שגיאה במחיקת קובץ: {e}")

    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_images():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    uploaded_files = request.files.getlist('photos')

    if not uploaded_files or uploaded_files[0].filename == '':
        return """
        <html dir="rtl"><body style="font-family:Arial; text-align:center; padding:50px;">
            <h2 style="color:#e94560;">שגיאה: לא נבחרו קבצים להעלאה</h2>
            <a href="/">חזרה</a>
        </body></html>
        """, 400

    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

    folder_path = os.path.abspath(UPLOAD_FOLDER)

    # תיקון: הכל רץ פעם אחת בלבד (היו קריאות כפולות)
    images_data = extract_all(folder_path)

    if not images_data:
        return """
        <html dir="rtl"><body style="font-family:Arial; text-align:center; padding:50px;">
            <h2 style="color:#e94560;">לא נמצאו תמונות בקבצים שהועלו</h2>
            <a href="/">חזרה</a>
        </body></html>
        """, 400

    map_html = create_map(images_data)
    timeline_html = create_timeline(images_data)
    analysis = analyze(images_data)
    report_html = create_report(images_data, map_html, timeline_html, analysis)

    return report_html


if __name__ == '__main__':
    app.run(debug=True)
