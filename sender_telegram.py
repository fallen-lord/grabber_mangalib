# import time
from img2pdf import convert
# import requests
# import PIL

from gsheet import *
from base_async import main
from teleg import *


def if_last_none(img_binaries):
    if img_binaries[-1] == b'':
        img_binaries.pop()
        if_last_none(img_binaries)

    return img_binaries


def get_images(chapter):
    global img_url
    img_links = [
        img_url + chapter[1] + "/" + img
        for img in chapter[-1]
    ]
    # print(img_links)
    images = main(img_links)

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


def send_chapters(chapters, start=1, count=10):

    for i, chapter in enumerate(chapters):

        if chapter[5].isnumeric():
            start = i + 2
            # print(chapter, start)
            break

    stop = start + count - 2

    for i, chapter in enumerate(chapters[start - 2:stop]):
        chapter[5] = start + i
        chapter[-1] = chapter[-1].split(",")

        # start_time = time.time()

        send(chapter)

        # print(f"\nUmumiy ketgan vaqt!!! ( ketgan vaqt {time.time() - start_time} s)\n")


def send_manga(manga_slug):

    chapters = get_chapters()

    start = 3
    count = 100
    global img_url
    img_url = MAIN_IMG_DOMAIN + "/manga/" + manga_slug + "/chapters/"

    send_chapters(chapters, start, count)


def start_sending(count=None):
    manga_list = get_manga_list()
    manga_list = manga_list[15:]
    manga_list = list(filter(lambda manga: (manga[6] != "completed" and manga[6] != "abandoned"), manga_list))
    if not count:
        manga_list = manga_list[:count]

    for i, manga in enumerate(manga_list):
        send_manga(manga[1])



if __name__ == "__main__":
    send_manga("")