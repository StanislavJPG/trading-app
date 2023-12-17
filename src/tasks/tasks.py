from celery import Celery
import smtplib
from email.message import EmailMessage

from src.config import CELERY_PASS, CELERY_MAIL, REDIS_PORT, REDIS_HOST

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465


celery = Celery('tasks', broker=f"redis://{REDIS_HOST}:{REDIS_PORT}")


def get_email_template_dashboard(username: str, user_email: str, operations: list):
    email = EmailMessage()
    email['Subject'] = 'Звіт'
    email['From'] = CELERY_MAIL
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: blue flex-col items-center"> Вітаю, {username}, ось твій звіт! </h1>'
        f'<h1 style="color: blue flex-col items-center"> Вітаю, {operations}, ось твій звіт! </h1>'
        # f'<h1 style="color: black;"> {["Тип інструменту: " + x["type"] + ", Кількість: " + x["quantity"] + ", Дата: " + str(x["date"])[:-7] for x in operations]}'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str, user_email: str, operations: list):
    email = get_email_template_dashboard(username, user_email, operations)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(CELERY_MAIL, CELERY_PASS)
        server.send_message(email)
