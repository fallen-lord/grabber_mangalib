import time

from selenium import webdriver

from jscode import fetch_list_manga, fetch_chapter
from consts import MAIN_DOMAIN
from gsheet import set_data, set_chapter, get_chapters


cService = webdriver.ChromeService(executable_path='sources/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=cService)


# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# driver = webdriver.Chrome(options=options)

mangaurl = lambda manga_slug: MAIN_DOMAIN + manga_slug + "/"

import json

def extract_pages_from_html(html_content):
    # Find the start and end index of the script content
    start_index = html_content.find('window.__pg = [')
    end_index = html_content.find('"}];', start_index) + 3

    # Extract the content between start and end index
    script_content = html_content[start_index:end_index]

    # print(script_content)
    # Remove "window.__pg = " to get valid JSON
    json_string = script_content.replace('window.__pg = ', '').strip(';')

    # Parse the JSON string to a Python object
    json_object = json.loads(json_string)

    return json_object

def collect_img_slug(pages):
    pages_slug = ""

    for page in pages:
        pages_slug += page['u'] + ","

    return pages_slug

def split_list(input_list, chunk_size=50):
    """
    Split a list into sublists of a specified size.

    Parameters:
    - input_list: The list to be split.
    - chunk_size: The size of each sublist.

    Returns:
    A list of sublists.
    """
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

#

def chapter_by_js(chapter_url):
    driver.execute_script(
        fetch_chapter
      + "fetchData('"
      + chapter_url
      + "');"
      )
    # time.sleep(1)
    chapter_page_html = ""

    while not chapter_page_html:
        chapter_page_html = driver.execute_script("return document.next_page;")

    pages = extract_pages_from_html(chapter_page_html)
    return pages


def chapter_by_driver(chapter_url):
    driver.get(chapter_url)
    pages = driver.execute_script("return window.__pg;")
    return pages

def info_chapter(chapter):
    start_time = time.time()

    # pages = chapter_by_driver(chapter['url'])
    pages = chapter_by_js(chapter['url'])

    finish_time = time.time() - start_time
    print(f"tmie for single chapter: {finish_time} s", chapter['number_row'])

    pages_slug = collect_img_slug(pages)


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


def chapter_group(chapters, start):

    for i, chapter in enumerate(chapters):
        chapter['number_row'] = start + i + 2
        chapter['url'] = (
                manga_url
                + "v"
                + str(chapter["chapter_volume"])
                + "/c"
                + chapter['chapter_number']
                + "?page=1")
        info_chapter(chapter)


def split_chapters(chapters, start, stop):
    chapters_list = split_list(chapters)
    for chapters in chapters_list:
        print(chapters, len(chapters))
        chapter_group(chapters, start)
        # for i, chapter in enumerate(chapters[start:stop]):
        #     chapter['number_row'] = start + i + 2
        #     chapter['url'] = (
        #             manga_url
        #             + "v"
        #             + str(chapter["chapter_volume"])
        #             + "/c"
        #             + chapter['chapter_number']
        #             + "?page=1")
        #     info_chapter(chapter)


def set_manga(manga_slug, start=1, count=10, continue_download=True):
    # start -= 1
    global manga_url
    manga_url = mangaurl(manga_slug)

    chapters = manga_info(manga_url)

    if continue_download and chapters != []:
        start = len(get_chapters())

    stop = start + count
    chapters.reverse()
    # split_chapters(chapters, start, stop)

    for i, chapter in enumerate(chapters[start:stop]):
        chapter['number_row'] = start + i + 2
        chapter['url'] = (
                manga_url
                + "v"
                + str(chapter["chapter_volume"])
                + "/c"
                + chapter['chapter_number']
                + "?page=1")
        info_chapter(chapter)


def list_page(page):
    driver.execute_script(fetch_list_manga + f"list_manga({page})")
    time.sleep(1)
    items = driver.execute_script("return document.rrd;")
    print(items)
    manga_list = items.get("items").get("data")
    for manga in manga_list:
        # print(manga)
        set_data(manga)


def set_manga_list():
    driver.get("https://mangalib.me/manga-list?types[]=1")
    for i in range(1, 10):
        list_page(i)


def main():
    manga_slug = "wo-laopo-shi-mowang-darren"
    set_manga(manga_slug, count=30)
    # set_manga_list()


if __name__ == "__main__":
    try:

        start_time = time.time()

        main()

        finish_time = time.time() - start_time
        print(f"\n\n\n yuklab olsih uchun ketgan vaqt: {finish_time} s")

    except Exception as e:

        driver.close()
        driver.quit()

        print("\n\nRaised Exception\n\n")
        print(e)

        raise e

    finally:

        driver.close()
        driver.quit()
