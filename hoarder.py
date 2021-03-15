from rStuff import rBot
from info import useragent, client_id, client_secret, bot_username, bot_pass
from HashDatabase import HashDatabase
from HashCollector import HashCollector


def collect_hashes():
    hash_collector_bot = rBot(useragent, client_id, client_secret, bot_username, bot_pass)
    hash_db = HashDatabase()
    hashcollector = HashCollector(hash_collector_bot, hash_db)
    hashcollector.start_collectin()


if __name__ == "__main__":
    collect_hashes()
