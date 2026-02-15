from report import create_report
from flask import Flask, render_template, request
import os

# הוספנו הגדרה מפורשת לתיקיית ה-templates
app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads' # שם התיקייה שבה נשמור את התמונות

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
def index():
    """הפונקציה הזו מציגה את דף הבית (הטופס) כשנכנסים לאתר"""
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
    folder_path = UPLOAD_FOLDER

    # מכאן הקוד ממשיך כרגיל לשאר הצוותים...
    images_data = fake_extract_all(folder_path)
    map_html = fake_create_map(images_data)
    timeline_html = fake_create_timeline(images_data)
    analysis = fake_analyze(images_data)
    report_html = create_report(images_data, map_html, timeline_html, analysis)

    return report_html

if __name__ == '__main__':
    # הפעלת השרת
    app.run(debug=True)