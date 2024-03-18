def imgs_to_pdf(img_binaries):
    # print(img_binaries[-1])

    try:

        pdf_file = convert(img_binaries[:len(img_binaries) - 2])

    except:

        from PIL import Image
        from io import BytesIO

        print("PIL ishlamoqda")

        images = [
            Image.open(BytesIO(img))
            for img in img_binaries[:20]
        ]

        images[0].save(
            "sources/test_chapter.pdf", "PDF", save_all=True, append_images=images[1:]
        )

    return pdf_file


def get_images(chapter):
    img_links = [
        IMG_URL + chapter[1] + "/" + img
        for img in chapter[-1]
    ]

    images = asyncio.run(main_async(img_links, get_img))

    if images == []:
        raise Exception(f"Chapter {chapter[3]} da XATOLIK YUZAGA keldi")

    # print(images)

    return [image[1].content for image in images[:-2]]


def send(chapter):
    start_time = time.time()

    img_binaries = get_images(chapter)

    # print(chapter)

    print(f"Yuklab olindi!!! (yuklab olishga ketgan vaqt {time.time() - start_time} s)")

    start_time = time.time()

    # print(img_binaries)

    pdf_file = imgs_to_pdf(img_binaries)

    print(f"\timg - > pdf ( ketgan vaqt {time.time() - start_time} s)")  # dddddddddddddddddddd

    chapter.append(pdf_file)

    start_time = time.time()

    send_file(chapter)

    print(f"Jo'natilindi!!! ( ketgan vaqt {time.time() - start_time} s)")


def send_chapters(chapters, start=1, count=10):
    start -= 2
    stop = start + count
    # print(chapters[start:], start, stop)

    for chapter in chapters[start:stop]:
        chapter[-1] = chapter[-1].split(",")[:-1]

        # print(chapter)
        send(chapter)


def lambda_handler(event=None, context=None):
    chapters = get_chapters(MANGA_SLUG)

    start = 149

    # print(chapters)

    send_chapters(chapters, 149, count=1)

    response = {
        "statusCode": 200,
        "body": "hello"
    }

    return response


if __name__ == "__main__":
    lambda_handler()
import time

from img2pdf import convert

from async_worker import *
from gsheet import *
from teleg import *


def imgs_to_pdf(img_binaries):
    # print(img_binaries[-1])

    try:

        pdf_file = convert(img_binaries[:len(img_binaries) - 2])

    except:

        from PIL import Image
        from io import BytesIO

        print("PIL ishlamoqda")

        images = [
            Image.open(BytesIO(img))
            for img in img_binaries[:20]
        ]

        images[0].save(
            "sources/test_chapter.pdf", "PDF", save_all=True, append_images=images[1:]
        )

    return pdf_file


def get_images(chapter):
    img_links = [
        IMG_URL + chapter[1] + "/" + img
        for img in chapter[-1]
    ]

    images = asyncio.run(main_async(img_links, get_img))

    if images == []:
        raise Exception(f"Chapter {chapter[3]} da XATOLIK YUZAGA keldi")

    # print(images)

    return [image[1].content for image in images[:-2]]


def send(chapter):
    start_time = time.time()

    img_binaries = get_images(chapter)

    # print(chapter)

    print(f"Yuklab olindi!!! (yuklab olishga ketgan vaqt {time.time() - start_time} s)")

    start_time = time.time()

    # print(img_binaries)

    pdf_file = imgs_to_pdf(img_binaries)

    print(f"\timg - > pdf ( ketgan vaqt {time.time() - start_time} s)")  # dddddddddddddddddddd

    chapter.append(pdf_file)

    start_time = time.time()

    send_file(chapter)

    print(f"Jo'natilindi!!! ( ketgan vaqt {time.time() - start_time} s)")


def send_chapters(chapters, start=1, count=10):
    start -= 2
    stop = start + count
    # print(chapters[start:], start, stop)

    for chapter in chapters[start:stop]:
        chapter[-1] = chapter[-1].split(",")[:-1]

        # print(chapter)
        send(chapter)


def lambda_handler(event=None, context=None):
    chapters = get_chapters(MANGA_SLUG)

    start = 149

    # print(chapters)

    send_chapters(chapters, 149, count=1)

    response = {
        "statusCode": 200,
        "body": "hello"
    }

    return response


if __name__ == "__main__":
    lambda_handler()
