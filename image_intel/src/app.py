from flask import Flask, render_template, request
import os

# הוספנו הגדרה מפורשת לתיקיית ה-templates
app = Flask(__name__, template_folder='templates')

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
    """הפונקציה הזו מופעלת כשהמשתמש לוחץ על 'נתח תמונות'"""
    # מקבלים את הנתיב שהמשתמש הקליד
    folder_path = request.form.get('folder_path')

    # בודקים שהמשתמש באמת הכניס משהו
    if not folder_path or not os.path.isdir(folder_path):
        return "אנא הכנס נתיב לתיקייה", 400

    # כשהצוותים יסיימו, נחליף את הקידומת 'fake_' בייבוא האמיתי של הקבצים שלהם!

    # שלב 1: שליפת נתונים (צוות 1, זוג A)
    images_data = fake_extract_all(folder_path)

    # שלב 2: יצירת מפה (צוות 1, זוג B)
    map_html = fake_create_map(images_data)

    # שלב 3: ציר זמן (צוות 2, זוג A)
    timeline_html = fake_create_timeline(images_data)

    # שלב 4: ניתוח (צוות 2, זוג B)
    analysis = fake_analyze(images_data)

    # שלב 5: הרכבת דו"ח (צוות 3, זוג B - השותפים שלך לרביעייה!)
    report_html = fake_create_report(images_data, map_html, timeline_html, analysis)

    # מחזירים למשתמש את הדו"ח הסופי
    return report_html


if __name__ == '__main__':
    # הפעלת השרת
    app.run(debug=True)