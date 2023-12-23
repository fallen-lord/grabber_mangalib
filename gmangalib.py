import time

from selenium import webdriver

from jscode import someCode
from consts import MAIN_DOMAIN
from gsheet import set_data, set_chapter, get_chapters

cService = webdriver.ChromeService(executable_path='sources/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=cService)


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# driver = webdriver.Chrome(options=options)

mangaurl = lambda manga_slug: MAIN_DOMAIN + manga_slug + "/"

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

    manga_url = mangaurl(manga_slug)

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


def list_page(page):
    driver.execute_script(someCode + f"list_manga({page})")
    time.sleep(1)
    items = driver.execute_script("return document.rrd;")
    print(items)
    manga_list = items.get("items").get("data")
    for manga in manga_list:
        # print(manga)
        set_data(manga)


def set_manga_list():
    driver.get("https://mangalib.me/manga-list?types[]=6")
    for i in range(1, 10):
        list_page(i)

def main():
    # manga_slug = "wo-laopo-shi-mowang-darren"
    # set_manga(manga_slug, count=10)
    set_manga_list()


if __name__ == "__main__":
    try:

        start_time = time.time()

        main()


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
