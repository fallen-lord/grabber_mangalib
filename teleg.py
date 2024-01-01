from requests import Session

from gsheet import *
from consts import MAIN_IMG_DOMAIN, BOT_URL, SOURCE_CHANEL, MAIN_CHANEL
# from gsheet import add_file_id

session = Session()


url_document = BOT_URL + "sendDocument"

def send_file(chapter, manga_channel=None):
    # print(chapter)

    url = BOT_URL + "sendDocument"
    data = {"chat_id": SOURCE_CHANEL}
    files = {"document": (f"Chapter {chapter[3]}.pdf", chapter[-1])}

    response = session.post(
        url,
        data=data,
        files=files
    )

    file_id = response.json()
    # print(file_id)
    file_id = file_id['result']['document']['file_id']
    add_file_id(chapter, file_id)

    if not manga_channel:
        manga_channel = MAIN_CHANEL

    session.post(
        url,
        data={"chat_id": manga_channel, "document": file_id}
    )


def send_files_id(files, manga_channel):
    for file in files:
        chapter_row = file[1]
        file_id = file[-1]
        # add_file_id(chapter_row, file_id)
        session.post(url_document, data={"chat_id": manga_channel, "document": file_id})

