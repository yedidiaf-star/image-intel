from extractor import extract_all
from report import create_report
from analyzer import analyze
from  timeline import create_timeline
from map_view import create_map
from flask import Flask, render_template, request
import os

# הוספנו הגדרה מפורשת לתיקיית ה-templates

app = Flask(__name__, template_folder='templates')

# --- השינוי הראשון: נתיב חכם לתיקיית images ---
# __file__ הוא המיקום של app.py. אנחנו עולים שתי רמות למעלה כדי להגיע לתיקייה הראשית של הפרויקט

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# עכשיו אנחנו מחברים את הנתיב הראשי לתיקיית images/uploads

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'images', 'uploads')

# --- פונקציות דמה (Fake) כדי שלא נצטרך לחכות לצוותים האחרים ---
def fake_extract_all(folder_path):
    return [
        {"filename": "test.jpg", "has_gps": True, "latitude": 32.0, "longitude": 34.7, "camera_model": "FakeCamera"}]


def fake_create_map(images_data):
    return "<div style='background:#e0e0e0; padding:20px;'><h3>כאן תופיע המפה של זוג B (צוות 1)</h3></div>"


def fake_create_timeline(images_data):
    return "<div style='background:#d0e0ff; padding:20px;'><h3>כאן יופיע ציר הזמן של זוג A (צוות 2)</h3></div>"


def fake_analyze(images_data):
    return {"total_images": 1, "images_with_gps": 1, "unique_cameras": ["FakeCamera"], "insights": ["זוהי תובנת דמה"]}


def fake_create_report(images_data, map_html, timeline_html, analysis):
    return f"""
    <html lang="he" dir="rtl">
        <body style="font-family: Arial; text-align: center;">
            <h1>דו"ח מודיעיני זמני</h1>
            <p>נבדקה התיקייה: {request.form.get('folder_path')}</p>
            {map_html}
            {timeline_html}
            <a href="/">חזור לדף הבית</a>
        </body>
    </html>
    """


# -----------------------------------------------------------

@app.route('/')
@app.route('/')
def index():
    """הפונקציה הזו מופעלת כשנכנסים לדף הבית. כאן נוסיף את הניקוי."""

    # בודקים אם התיקייה בכלל קיימת
    if os.path.exists(UPLOAD_FOLDER):
        # עוברים על כל הקבצים שנמצאים כרגע בתיקייה
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                # מוודאים שזה באמת קובץ (ולא תיקייה פנימית) ומוחקים אותו
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"שגיאה במחיקת קובץ: {e}")

    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_images():
    # א. יצירת התיקייה בשרת אם היא לא קיימת
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # ב. משיכת רשימת הקבצים שהועלו מהדפדפן
    uploaded_files = request.files.getlist('photos')

    # ג. בדיקה שהמשתמש אכן בחר קבצים
    if not uploaded_files or uploaded_files[0].filename == '':
        return "שגיאה: לא נבחרו קבצים להעלאה", 400

    # ד. לולאה ששומרת כל קובץ פיזית לתוך תיקיית ה-uploads
    for file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

    # ה. שליחת הנתיב של התיקייה שלנו לשאר המודולים
    folder_path = os.path.abspath(UPLOAD_FOLDER)

    # מכאן הקוד ממשיך כרגיל לשאר הצוותים...
    images_data = extract_all(folder_path)
    map_html = create_map(images_data)
    timeline_html = create_timeline(images_data)
    analysis = analyze(images_data)
    report_html = create_report(images_data, map_html, timeline_html, analysis)

    return report_html

if __name__ == '__main__':
    # הפעלת השרת
    app.run(debug=True)