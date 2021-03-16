from dotenv import load_dotenv
from os import environ

load_dotenv()

DATABASE_URL = environ.get("DATABASE_URL")

SENTRY_DSN = environ.get("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(environ.get("SENTRY_TRACES_SAMPLE_RATE", "1.0"))

useragent = environ.get("useragent")
client_id = environ.get("client_id")
client_secret = environ.get("client_secret")
bot_username = environ.get("bot_username")
bot_pass = environ.get("bot_pass")
