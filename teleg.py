from requests import Session

from gsheet import *
from consts import MAIN_IMG_DOMAIN, BOT_URL, SOURCE_CHANEL
# from gsheet import add_file_id

session = Session()


url_document = BOT_URL + "sendDocument"

def send_file(chapter, manga_channel=None):
    # print(chapter)
    file_name = f"Том {chapter[4]} Глава {chapter[3]}.pdf"
    url = BOT_URL + "sendDocument"
    data = {"chat_id": SOURCE_CHANEL}
    files = {"document": (file_name, chapter[-1])}

    response = session.post(
        url,
        data=data,
        files=files
    )

    file_id = response.json()
    # print(file_id)
    file_id = file_id['result']['document']['file_id']
    add_file_id(chapter, file_id)

    # if not manga_channel:
    #     manga_channel = MAIN_CHANEL

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


def set_chat_photo(chat_id, photo):

    url = BOT_URL + "setChatPhoto"

    if isinstance(photo, str):
        photo = session.get(photo).content

    params = {
        "chat_id": chat_id,
    }
    file = {
        "photo": ("photo.jpg", photo)
    }

    response = session.post(url, data=params, files=file)

    if response.status_code > 299:
        print(response.status_code)
        print(response.text)
    else:
        print("Photo set successfully")

if __name__ == "__main__":
    set_chat_photo("-1002031876266", "https://cover.imglib.info/uploads/cover/i-alone-level-up/cover/MqLYFST4k4mY_250x350.jpg")
