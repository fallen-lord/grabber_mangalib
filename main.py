# import time
from img2pdf import convert

from base_async import main, get_img
from gsheet import get_chapters
from teleg import *


def if_last_none(img_binaries):
    if img_binaries[-1] == b'':
        img_binaries.pop()
        if_last_none(img_binaries)

    return img_binaries


def get_images(chapter):
    img_links = [
        IMG_URL + chapter[1] + "/" + img
        for img in chapter[-1]
    ]
    # print(img_links)

    # Beginning Async programming

    images = main(img_links, get_img)

    if images == []:
        raise Exception(f"Chapter {chapter[3]} da XATOLIK YUZAGA keldi")

    # print(images)

    return [image[1] for image in images]


def send(chapter):
    # start_time = time.time()

    img_binaries = get_images(chapter)

    img_binaries = if_last_none(img_binaries)

    # print(f"Yuklab olindi!!! ( {time.time() - start_time} s)")

    # start_time = time.time()

    # print(img_binaries)
    # print(chapter)

    pdf_file = convert(img_binaries)

    # print(f"\timg - > pdf ( ketgan vaqt {time.time() - start_time} s)")

    chapter.append(pdf_file)

    # start_time = time.time()

    send_file(chapter)

    # print(f"Jo'natilindi!!! ( ketgan vaqt {time.time() - start_time} s)")


def send_chapters(chapters, start=1, count=10, continue_sending=False):
    if continue_sending:

        for i, chapter in enumerate(chapters):

            if chapter[5].isnumeric():
                start = i + 2
                # print(chapter, start)
                break

    stop = start + count - 2

    for i, chapter in enumerate(chapters[start - 2:stop]):
        chapter[5] = start + i
        chapter[-1] = chapter[-1].split(",")[:-1]

        # start_time = time.time()

        send(chapter)

        # print(f"\nUmumiy ketgan vaqt!!! ( ketgan vaqt {time.time() - start_time} s)\n")


def lambda_handler():
    chapters = get_chapters()

    continue_sending = True
    start = 3
    count = 100

    send_chapters(chapters, start, count, continue_sending=continue_sending)


if __name__ == "__main__":
    lambda_handler()
