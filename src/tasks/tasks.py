from celery import Celery
import smtplib
from email.message import EmailMessage

from src.config import CELERY_PASS, CELERY_MAIL, REDIS_PORT, REDIS_HOST

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465


celery = Celery('tasks', broker=f"redis://{REDIS_HOST}:{REDIS_PORT}")


def get_email_template_dashboard(username: str, user_email: str):
    email = EmailMessage()
    email['Subject'] = 'Звіт'
    email['From'] = CELERY_MAIL
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: blue;"> Вітаю, {username}, ось твій звіт! </h1>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str, user_email: str):
    email = get_email_template_dashboard(username, user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(CELERY_MAIL, CELERY_PASS)
        server.send_message(email)
