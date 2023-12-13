from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
import time

cService = webdriver.ChromeService(executable_path='sources/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=cService)
# driver = 0
# from selenium import webdriver

# import time

from consts import *
from gsheet import set_data, set_chapter

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


def manga_info():
    """Manga haqidagi ma'lumotni googlesheet ga joylaydigan funksiya"""

    driver.get(MANGA_URL)

    all_data = driver.execute_script("return window.__DATA__;")
    # print(all_data)

    set_data(all_data['manga'])

    return all_data['chapters']['list']


def main(start=1, stop=None, count=10):
    start -= 1
    if stop == None:
        stop = start + count
    else:
        count = stop - start - 1

    # print(22222222)
    chapters = (manga_info())
    chapters.reverse()
    # import json
    # print(json.dumps(chapters, indent=4,))

    for i, chapter in enumerate(chapters[start:stop]):
        chapter['number_row'] = start + i + 2
        info_chapter(chapter)
    # print(start + i + 2)


if __name__ == "__main__":
    try:

        start = 11

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