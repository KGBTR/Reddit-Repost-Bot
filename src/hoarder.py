from environ import (
    SENTRY_DSN,
    SENTRY_TRACES_SAMPLE_RATE,
)
from HashDatabase import HashDatabase
from HashCollector import HashCollector
import sentry_sdk

if __name__ == "__main__":
    sentry_sdk.init(
        SENTRY_DSN,
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
    )

    hash_db = HashDatabase()
    hashcollector = HashCollector(hash_db)
    hashcollector.start_collectin()
