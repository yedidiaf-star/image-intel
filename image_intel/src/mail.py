import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from אינדקסים import my_string

load_dotenv()
def send_custom_email(target_email, email_body):
    MY_EMAIL = os.getenv("EMAIL_USER")
    MY_PASSWORD = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = "הודעה חשובה מהמערכת"
    msg['From'] = MY_EMAIL
    msg['To'] = target_email
    msg.set_content(email_body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MY_EMAIL, MY_PASSWORD)
            server.send_message(msg)
            print(f"המייל נשלח בהצלחה ל-{target_email}!")
    except Exception as e:
        print(f"קרתה תקלה: {e}")
send_custom_email("kaplinnetanel10@gmail.com", "שלום! הצלחתי להפעיל את הפונקציה.")