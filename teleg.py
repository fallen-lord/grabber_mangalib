from requests import Session

from consts import MAIN_IMG_DOMAIN, BOT_URL, SOURCE_CHANEL, MAIN_CHANEL
from gsheet import add_file_id

session = Session()


def send_file(chapter):
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

    session.post(
        url,
        data={"chat_id": MAIN_CHANEL, "document": file_id}
    )


