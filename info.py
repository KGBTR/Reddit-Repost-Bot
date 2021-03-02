from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']

useragent = os.environ["useragent"]
client_id = os.environ["client_id"]
client_secret = os.environ["client_secret"]
bot_username = os.environ["bot_username"]
bot_pass = os.environ["bot_pass"]
