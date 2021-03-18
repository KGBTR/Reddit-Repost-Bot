from dotenv import load_dotenv
from os import getenv

load_dotenv()

#LOGGER LEVEL
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

#PRODUCTION
PY_ENV = getenv("PY_ENV", "development")

#POSTRGRES DB
DATABASE_URL = getenv("DATABASE_URL")

#SENTRY
SENTRY_USE = getenv("SENTRY_USE", "False")
if SENTRY_USE == "True" or SENTRY_USE == "true" or SENTRY_USE == "1":
  SENTRY_USE = True
else:
  SENTRY_USE = False

SENTRY_DSN = getenv("SENTRY_DSN")
SENTRY_TRACES_SAMPLE_RATE = float(getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0"))

#REDDIT API
useragent = getenv("useragent")
client_id = getenv("client_id")
client_secret = getenv("client_secret")
bot_username = getenv("bot_username")
bot_pass = getenv("bot_pass")