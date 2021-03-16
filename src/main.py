from rStuff import rBot
from info import (
    useragent,
    client_id,
    client_secret,
    bot_username,
    bot_pass,
    SENTRY_DSN,
    SENTRY_TRACES_SAMPLE_RATE,
)
from HashDatabase import HashDatabase
from MainWorker import MainWorker
import sentry_sdk

if __name__ == "__main__":
    sentry_sdk.init(
        SENTRY_DSN,
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
    )

    reverse_img_bot = rBot(useragent, client_id, client_secret, bot_username, bot_pass)
    hash_db = HashDatabase()
    mainworker = MainWorker(reverse_img_bot, hash_db)
    mainworker.start_working()
