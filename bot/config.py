import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
WEBAPP_URL = os.getenv(
    "WEBAPP_URL",
    "https://odwillio0702.github.io/personalinfo/"
)