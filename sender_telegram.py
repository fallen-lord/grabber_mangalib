import time
import gc

from img2pdf import convert
# import requests
# import PIL

from gsheet import *
import mixins
import project_async
import async_worker
from teleg import *


def create_manga_channel(manga):
    import channels
    channel_id = channels.make_private_channel(channel_title=manga[4])
    channel_id = "-100" + str(channel_id)
    manga[3] = channel_id
    update_status(manga[0], ("channel_id", channel_id))
    set_chat_photo(channel_id, manga[5])
    update_status(manga[0], ("channel_photo", "set"))
    manga[6] = "set"

def if_last_none(img_binaries):
    if not img_binaries:  # Check if the list is empty
        return None
    # print(img_binaries)
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
    ]
    # print(group)

    chapter_binaries = async_worker.sync_process_links(chapter_links, project_async.chapter_img, 20, value_type=bytes, print_error_links=True)

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
        # print(chapter[0], chapter[1], len(chapter[-1]))
        chapter[-1] = convert(if_last_none(chapter[-1]))

    # gc.collect()

    files_id = async_worker.sync_process_links(chapters, project_async.send_main_channel, value_type=bytes, print_error_links=True)
    # for i in files_id:
    #   print(i)
    global manga_channel

    add_files_id(files_id)

    send_files_id(files_id, manga_channel)

    # Perform garbage collection
    gc.collect()


def get_images(chapter, manga=None):
    global img_url
    # if manga:
    #     img_url = manga[-1]
    # else:
    #     global img_url
    img_links = [
        img_url + chapter[1] + "/" + img
        for img in chapter[-1]
            if mixins.check_to_latin(img)
    ]
    # print(img_links)
    images = async_worker.sync_process_links(img_links, project_async.get_img, value_type=bytes, print_error_links=True)

    if images == []:
        raise Exception(f"Chapter {chapter[3]} da XATOLIK YUZAGA keldi")

    # print(images)
    return images
    # return [image[1] for image in images]


def send(chapter, i=0, manga=None):
    start_time = time.time()
    img_binaries = get_images(chapter, manga)

    print(f"Yuklab olindi!!! ( {time.time() - start_time} s)")

    try:
        img_binaries = if_last_none(img_binaries)
        pdf_file = convert(img_binaries)

        chapter.append(pdf_file)

        # start_time = time.time()
        manga_channel = manga[3]
        send_file(chapter, manga_channel)

    except:
        print("XATOLIK YU")
        if i < 5:
            i += 1
            send(chapter, i, manga)
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


def send_chapters(chapters, start=1, count=None, manga=None):
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


    for chapter in chapters:
        start_time = time.time()

        send(chapter, manga=manga)

        print(f"\nUmumiy ketgan vaqt!!! ( ketgan vaqt {time.time() - start_time} s)\n")

    # chunk_size = 1
    # chapter_group = mixins.split_list(chapters, chunk_size=chunk_size)
    # for group in chapter_group:
    #     # for chapter in group:
    #     #     print(chapter[:-1], len(chapter[-1]))
    #     start_time = time.time()
    #     send_group(group)
    #     print(f"\nUmumiy ketgan vaqt!!! ( ketgan vaqt {time.time() - start_time} s)\n")
        # break

    #     # print(len(group))
    #     print()
    #     # break


def send_manga(manga):
    manga_slug = manga[0]
    chapters = get_chapters(manga_slug)
    # print(manga)
    if manga[3] == "":
        create_manga_channel(manga)
    if manga[6] == "":
        set_chat_photo(manga[3], manga[5])
        update_status(manga[0], ("channel_photo", "set"))

    start = 1
    count = None
    global img_url
    img_url = MAIN_IMG_DOMAIN + "/manga/" + manga_slug + "/chapters/"
    manga.append(img_url)

    if manga[2] == "":
        update_status(manga_slug, ("sending", "started"))
    start_time = time.time()

    send_chapters(chapters, start, count, manga)

    finish_time = time.time() - start_time
    print(f"\nUmumiy ketgan vaqt!!! ( ketgan vaqt {finish_time} s)\n")
    # if finish_time < 10:
        # time.sleep(1)
        # print("==========================================================")
    if __name__ != "__main__":
        update_status(manga_slug, ("sending", "completed"))


def start_sending(count_manga=None):
    manga_list = column_by_names("slug", "downloading", "sending", "channel_id", "rus_name", "coverImage", "channel_photo")

    for manga_data in manga_list:
        if (not manga_data[1] == "completed") or (manga_data[2] == "completed"):
            continue
        send_manga(manga_data)
    # for i, manga in enumerate(manga_list):
    #     send_manga(manga)
        # print(manga[1], manga[8], MAIN_CHANEL)


if __name__ == "__main__":
    start_sending(count_manga=1)