from dotenv import load_dotenv
from os import getenv

load_dotenv()

LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

DATABASE_URL = getenv("DATABASE_URL")

SENTRY_DSN = getenv("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0"))

useragent = getenv("useragent")
client_id = getenv("client_id")
client_secret = getenv("client_secret")
bot_username = getenv("bot_username")
bot_pass = getenv("bot_pass")
