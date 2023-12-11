from celery import Celery
import smtplib
from email.message import EmailMessage

from app.src.config import CELERY_PASS, CELERY_MAIL

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465


celery = Celery('tasks', broker='redis://localhost:6379//')


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'Звіт'
    email['From'] = CELERY_MAIL
    email['To'] = CELERY_MAIL

    email.set_content(
        '<div>'
        f'<h1 style="color: blue;"> Вітаю, {username}, ось твій звіт! </h1>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(CELERY_MAIL, CELERY_PASS)
        server.send_message(email)
