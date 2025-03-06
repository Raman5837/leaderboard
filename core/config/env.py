from os import environ

from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = environ.get("REDIS_PORT")
REDIS_DB = int(environ.get("REDIS_DB") or "0")
DJANGO_SECRET_KEY = environ.get("DJANGO_SECRET_KEY", "__")
