from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import time

from consts import MANGA_URL
from gsheet import set_data, set_chapter

cService = webdriver.ChromeService(executable_path='sources/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=cService)
# driver = 0
# from selenium import webdriver


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')


# driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()


def info_chapter(chapter):
    chapter_url = MANGA_URL + "v" + str(chapter["chapter_volume"]) + "/c" + chapter['chapter_number'] + "?page=1"
    driver.get(chapter_url)

    pages = driver.execute_script("return window.__pg;")

    pages_slug = ""

    for page in pages:
        pages_slug += page['u'] + ","

    # print(pages_slug)
    # print(chapter)
    chapter['pages'] = pages_slug
    set_chapter(chapter)


def manga_info(manga_url=MANGA_URL, manga_slug=MANGA_URL):
    """Manga haqidagi ma'lumotni googlesheet ga joylaydigan funksiya"""

    driver.get(manga_url)

    manga_data = driver.execute_script("return window.__DATA__;")
    print(manga_data)

    if manga_data["chapters"].get("list") == []:
        return

    set_data(manga_data['manga'])

    return manga_data['chapters']['list']


def main(start=1, stop=None, count=10):

    start -= 1

    if stop == None:
        stop = start + count
    else:
        count = stop - start - 1

    chapters = manga_info()
    if chapters is None:
        return
    chapters.reverse()

    for i, chapter in enumerate(chapters[start:stop]):

        chapter['number_row'] = start + i + 2
        info_chapter(chapter)


if __name__ == "__main__":
    try:

        start = 1

        main(start, count=10)

    except Exception as e:

        driver.close()
        driver.quit()

        print("\n\nRaised Exception\n\n")
        print(e)

        raise e

# finally:

# 	driver.close()
# 	driver.quit()
