
import os

MAIN_DOMAIN = "https://mangalib.me/"


TOP_MANGA = os.environ['SHEET_KEY']

GSHEET_KEY = TOP_MANGA


# MANGA_URL = MAIN_DOMAIN + MANGA_SLUG + '/'


MAIN_IMG_DOMAIN = 'https://img33.imgslib.link/'

# IMG_URL = MAIN_IMG_DOMAIN + "/manga/" + MANGA_SLUG + "/chapters/"

BOT_TOKEN = os.environ['BOT_TOKEN']

BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

SOURCE_CHANEL = os.environ['SOURCE_CHANEL']





API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']

SOURCE = "sources/"
SESSION_PATH =SOURCE + "sessions/"
SESSION_NAME = SESSION_PATH + "not_just"
# SESSION_NAME = SESSION_PATH + "my33_328_humans"
# CHANNEL_PATH = SOURCE + "channels/"
# IMAGES = SOURCE + "images/"

# MAIN_BOT = "https://t.me/mkclone_bot"
MAIN_BOT = "https://t.me/sender2chanel_bot"

# BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"


UPDATE_URL = BOT_URL + "getUpdates"

if __name__ == "__main__":
    print(UPDATE_URL)


