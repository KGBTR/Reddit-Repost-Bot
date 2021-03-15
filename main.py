from rStuff import rBot
from info import useragent, client_id, client_secret, bot_username, bot_pass
from HashDatabase import HashDatabase
from MainWorker import MainWorker


def run_bot():
    reverse_img_bot = rBot(useragent, client_id, client_secret, bot_username, bot_pass)
    hash_db = HashDatabase()
    mainworker = MainWorker(reverse_img_bot, hash_db)
    mainworker.start_working()


if __name__ == "__main__":
    run_bot()
    pass
