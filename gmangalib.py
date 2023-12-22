import time

from selenium import webdriver

from consts import MAIN_DOMAIN
from gsheet import set_data, set_chapter, get_chapters

cService = webdriver.ChromeService(executable_path='sources/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=cService)


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# driver = webdriver.Chrome(options=options)


def info_chapter(chapter):
    driver.get(chapter['chapter_url'])

    pages = driver.execute_script("return window.__pg;")

    pages_slug = ""

    for page in pages:
        pages_slug += page['u'] + ","

    chapter['pages'] = pages_slug
    set_chapter(chapter)


def manga_info(manga_url):
    """Manga haqidagi ma'lumotni googlesheet ga joylaydigan funksiya"""

    driver.get(manga_url)

    manga_data = driver.execute_script("return window.__DATA__;")
    # print(manga_data)
    if manga_data == None:
        return []

    chapters_list = manga_data.get("chapters").get('list')
    if chapters_list == []:
        return []

    set_data(manga_data['manga'])

    return chapters_list


def set_manga(manga_slug, start=1, count=10, continue_download=True):
    # start -= 1

    manga_url = MAIN_DOMAIN + manga_slug + "/"

    chapters = manga_info(manga_url)

    if continue_download and chapters != []:
        start = len(get_chapters())

    stop = start + count
    chapters.reverse()

    for i, chapter in enumerate(chapters[start:stop]):
        chapter['number_row'] = start + i + 2
        chapter['chapter_url'] = (
                manga_url
                + "v"
                + str(chapter["chapter_volume"])
                + "/c"
                + chapter['chapter_number']
                + "?page=1")
        info_chapter(chapter)


def main():
    manga_slug = "wo-laopo-shi-mowang-darren"
    set_manga(manga_slug, count=10)


if __name__ == "__main__":
    try:

        start_time = time.time()

        # main()

        driver.get("https://mangalib.me/manga-list?types[]=6")
        from jscode import someCode
        driver.execute_script(someCode + f"list_manga({5})")
        time.sleep(1)
        l = driver.execute_script("return document.rrd;")


        print(l)

        print(f"Yuklab olindi!!! ( {time.time() - start_time} s)")

        # a = driver.request('POST', 'url here', data={"param1": "value1"})

    except Exception as e:

        driver.close()
        driver.quit()

        print("\n\nRaised Exception\n\n")
        print(e)

        raise e

    finally:

        driver.close()
        driver.quit()
