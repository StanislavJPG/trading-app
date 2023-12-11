from dotenv import load_dotenv
import os


load_dotenv()


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT', default=9999)
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
SECRET_AUTH = os.environ.get('SECRET_AUTH')
SECRET_MANAGE = os.environ.get('SECRET_MANAGE')
CELERY_MAIL = os.environ.get('CELERY_MAIL')
CELERY_PASS = os.environ.get('CELERY_PASS')

DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')
