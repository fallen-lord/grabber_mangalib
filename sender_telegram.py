import time
from img2pdf import convert
# import requests
# import PIL

from gsheet import *
import mixins
import project_async
import base_async
from teleg import *


def if_last_none(img_binaries):
    if not img_binaries:  # Check if the list is empty
        return None

    if img_binaries[-1] == b'' or (b'html' in img_binaries[-1]):
        img_binaries.pop()
        if_last_none(img_binaries)

    # for img_binary in img_binaries:
    #   print(img_binary)
    # print(img_binaries[-1])
    return img_binaries


def send_group(group):
    chapter_links = [
        ((img_url + chapter[1] + "/" + img), chapter[5], chapter[3])
        for chapter in group
            for img in chapter[-1]
                if mixins.check_to_latin(img)
    ]
    # print(chapter_links)
    chapter_binaries = base_async.main(chapter_links, project_async.chapter_img)
    i = chapter_binaries[0][0][1]
    chapter_number = chapter_binaries[0][1]
    chapters = [[i, chapter_number, []]]
    for binary in chapter_binaries:
        chapter_number = binary[1]
        if binary[0][1] == i:
            chapters[-1][-1].append(binary[-1])
        else:
            i = binary[0][1]
            chapters.append([i, chapter_number, []])
            chapters[-1][-1].append(binary[-1])
        # print(i[:-1])
    # print(chapters[0][1][0])
    for chapter in chapters:
        print(chapter[0], chapter[1], len(chapter[-1]))


def get_images(chapter):
    global img_url
    img_links = [
        img_url + chapter[1] + "/" + img
        for img in chapter[-1]
        if mixins.check_to_latin(img)
    ]
    # print(img_links)
    images = base_async.main(img_links, project_async.get_img)

    if images == []:
        raise Exception(f"Chapter {chapter[3]} da XATOLIK YUZAGA keldi")

    # print(images)

    return [image[1] for image in images]


def send(chapter, i=0):
    start_time = time.time()

    img_binaries = get_images(chapter)

    print(f"Yuklab olindi!!! ( {time.time() - start_time} s)")

    # pdf_file = convert(img_binaries)

    # start_time = time.time()

    # print(img_binaries)
    # print(chapter)
    try:
        img_binaries = if_last_none(img_binaries)
        pdf_file = convert(img_binaries)

        chapter.append(pdf_file)

        # start_time = time.time()

        send_file(chapter, manga_channel)

    except:
        print("XATOLIK YU", img_binaries[-1])
        if i < 5:
            i += 1
            send(chapter, i)
        else:
            print(img_binaries)
            raise Exception("XATOLIK YUZAGA keldi")
        # pdf_file = convert(img_binaries[:-1])
    # for i in range(5):
    #   try:
    #     pdf_file = convert(img_binaries)
    #   except Exception as e:
    #     print(e, i)
    #     if i == 4:
    #       for j in range(len(img_binaries)):
    #         try:
    #           convert(img_binaries[j])
    #         except Exception as e:
    #           print(e, j)
    #           break
    #       pdf_file = convert
    #     continue
    #   break
    # print(f"\timg - > pdf ( ketgan vaqt {time.time() - start_time} s)")

    # print(f"Jo'natilindi!!! ( ketgan vaqt {time.time() - start_time} s)")



def send_chapters(chapters, start=1, count=None):
    for i, chapter in enumerate(chapters):

        if chapter[5].isnumeric():
            start = i
            # print(chapter, start)
            break

    if count:
        stop = start + count
    else:
        stop = len(chapters)

    chapters = chapters[start:stop]
    for i, chapter in enumerate(chapters):
        chapter[5] = start + i + 2
        chapter[-1] = chapter[-1].split(",")[:-1]

        # start_time = time.time()

        # send(chapter)
    chunk_size = 10
    chapter_group = mixins.split_list(chapters, chunk_size=chunk_size)
    for group in chapter_group:
        # for chapter in group:
        #     print(chapter[:-1], len(chapter[-1]))
        send_group(group)
        # print(len(group))
        print()
        break
        # print(f"\nUmumiy ketgan vaqt!!! ( ketgan vaqt {time.time() - start_time} s)\n")


def send_manga(manga):
    manga_slug = manga[1]
    chapters = get_chapters(manga_slug)
    global manga_channel
    manga_channel = manga[8]

    start = 1
    count = None
    global img_url
    img_url = MAIN_IMG_DOMAIN + "/manga/" + manga_slug + "/chapters/"

    if manga[6] == "not_started":
        update_status(manga_slug, (7, "started"))

    send_chapters(chapters, start, count)

    # if __name__ != "__main__":
    #     update_status(manga_slug, (7, "completed"))


def start_sending(count_manga=None):
    manga_list = get_manga_list()
    # manga_list = manga_list[13:]
    manga_list = list(filter(
        lambda manga: ((manga[6] == "started" or manga[6] == "not_started") and manga[8]), manga_list))
    if count_manga:
        manga_list = manga_list[:count_manga]

    for i, manga in enumerate(manga_list):
        send_manga(manga)
        # print(manga[1], manga[8], MAIN_CHANEL)



if __name__ == "__main__":
    start_sending(count_manga=1)