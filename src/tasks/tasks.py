from celery import Celery
import smtplib
from email.message import EmailMessage
from src.config import CELERY_PASS, CELERY_MAIL, REDIS_PORT, REDIS_HOST

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465


celery = Celery('tasks', broker=f"redis://{REDIS_HOST}:{REDIS_PORT}")


def get_email_template_dashboard(username: str, user_email: str, operations):
    email = EmailMessage()
    email['Subject'] = 'Звіт'
    email['From'] = CELERY_MAIL
    email['To'] = user_email

    email.set_content(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <style>
                @import url(https://fonts.googleapis.com/css?family=Didact+Gothic|Comfortaa:400,700&subset=latin,cyrillic);
                *, *:before, *:after {{
                    box-sizing: border-box;
                }}
                .wrap {{
                    position: relative;
                    margin: 50px auto;
                    text-align: center;
                    width: 380px;
                    height: 400px;
                    background: white;
                    padding: 30px 40px;
                    border: 1px solid rgba(0, 0, 0, .1);
                }}
                .wrap:before, .wrap:after {{
                    content: "";
                    position: absolute;
                    width: inherit;
                    height: inherit;
                    border: 1px solid rgba(0, 0, 0, .1);
                    background: white;
                }}
                .wrap:before {{
                    top: 5px;
                    left: -5px;
                    z-index: -1;
                }}
                .wrap:after {{
                    top: 10px;
                    left: -10px;
                    z-index: -2;
                }}
                .cat span {{
                    font-family: 'Comfortaa', cursive;
                    font-size: 13px;
                    text-transform: uppercase;
                    margin-bottom: 20px;
                    color: #ff6f5a;
                    font-weight: bold;
                }}
                h2 {{
                    font-family: 'Comfortaa', cursive;
                    font-size: 18px;
                    font-weight: 400;
                    margin-bottom: 16px;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    color: #333333;
                }}
                .public {{
                    font-family: 'Didact Gothic', sans-serif;
                    color: #999999;
                    font-size: 13px;
                }}
                p {{
                    font-family: 'Didact Gothic', sans-serif;
                    color: #555555;
                    font-size: 14px;
                    line-height: 22px;
                }}
                .more-button {{
                    font-family: 'Comfortaa', cursive;
                    color: #333333;
                    font-size: 11px;
                    padding-bottom: 8px;
                    display: inline-block;
                    margin: 35px 0 20px;
                    text-transform: uppercase;
                    position: relative;
                    font-weight: bold;
                    letter-spacing: 1px;
                    transition: .3s linear;
                }}
                .more-button:before {{
                    content: "";
                    position: absolute;
                    left: 50%;
                    margin-left: -20px;
                    bottom: 0;
                    height: 1px;
                    width: 40px;
                    background: #333333;
                    transition: .3s linear;
                }}
                .more-button:hover {{
                    color: #ff6f5a;
                }}
                .more-button:hover:before {{
                    background: #ff6f5a;
                }}
            </style>
            <title>Title</title>
        </head>
        <body>
            <div class="wrap">
                <div class="cat">
                    <span>Звіт</span>
                </div>
                <h2>{username}, ось ваш звіт:</h2>
                <div class="post">
                    <span class="public"> Вибірка дат: {(str([str(x['date'])[:-7] for x in operations])[1:-1]).replace("'", '')}</span>
                    <p style="font-weight: bold;">Операції:</p>
                    <p>{', '.join([str(operations.index(x) + 1) + ') ' + x['type'] for x in operations])}</p>
                    <p style="font-weight: bold;">Кількість:</p>
                    <p>{', '.join([str(operations.index(x) + 1) + ') ' + x['quantity'] for x in operations])}</p>
                </div>
            </div>
        </body>
        </html>
        """,
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str, user_email: str, operations):
    email = get_email_template_dashboard(username, user_email, operations)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(CELERY_MAIL, CELERY_PASS)
        server.send_message(email)
