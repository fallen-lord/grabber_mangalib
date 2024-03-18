import time

from selenium import webdriver
# import undetected_chromedriver as uc

from jscode import *
from mixins import *
from consts import MAIN_DOMAIN
from gsheet import set_data, set_chapter, get_chapters, set_chapters, update_status, get_manga_list

options = webdriver.ChromeOptions()
options.add_argument("disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
cService = webdriver.ChromeService(executable_path='sources/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=cService, options=options)

# options = uc.ChromeOptions()
# options.headless = False  # Set headless to False to run in non-headless mode
#
# driver = uc.Chrome(use_subprocess=True, options=options)

freeze = None
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# driver = webdriver.Chrome(options=options)

mangaurl = lambda manga_slug: MAIN_DOMAIN + manga_slug + "/"


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
    driver.get(chapter_url + "?section=chapters")
    pages = driver.execute_script("return window.__pg;")
    return pages


def info_chapter(chapter, return_data=False):
    start_time = time.time()

    # pages = chapter_by_driver(chapter['url'])
    pages = chapter_by_js(chapter['url'])

    finish_time = time.time() - start_time
    print(f"tmie for single chapter: {finish_time} s", chapter['number_row'])

    pages_slug = collect_img_slug(pages)


    chapter['pages'] = pages_slug
    if return_data:
        return chapter
    set_chapter(chapter)


def get_value(css_selector):
    from selenium.webdriver.common.by import By

    # Find the first div element with the specified class
    div_element = driver.find_element(By.CSS_SELECTOR, css_selector)

    # Get the text content of the div element
    value_text = div_element.text

    if value_text == "Продолжается":
        value_text = "continues"
    elif value_text == "Завершен":
        value_text = "completed"
    elif value_text == "Заморожен":
        value_text = "frozen"
    else:
        value_text = "abandoned"
    return value_text

def update_manga_status(manga: list):
    # print(manga)
    if manga[5] == "not_started":
        update_status(manga[0], (6, "started"))
    if len(manga) < 10:
        status_manga = get_value('div.media-info-list__value.text-capitalize')
        update_status(manga[0], (10, status_manga))


def manga_info(manga_slug):
    """Manga haqidagi ma'lumotni googlesheet ga joylaydigan funksiya"""

    driver.get(manga_url)
    # driver.maximize_window()
    # global freeze
    # if not freeze:
    #     time.sleep(30)
    #     freeze = True
    manga_data = driver.execute_script("return window.__DATA__;")

    if manga_data is None:
        update_status(manga_slug, (6, "abandoned"))
        return [], []
    chapters_list = manga_data.get("chapters").get('list')
    if chapters_list == []:
        update_status(manga_slug, (6, "abandoned"))
        return [], []

    manga = set_data(manga_data['manga'])
    update_manga_status(manga)


    return chapters_list, manga


def async_js(links: list):

    jscode = asyncJS + "main(" + json.dumps(links) + """)
  .then(results => document.async_pages = results.sort((a, b) => a[0] - b[0]))
  .catch(error => console.error('Error:', error));
    """
    # print(jscode)
    driver.execute_script(jscode, links)
    chapter_pages_html = None
    for i in range(100):

        chapter_pages_html = driver.execute_script("return document.async_pages;")
        if chapter_pages_html is not None:
            break
        time.sleep(0.4)
        # print(chapter_pages_html)

    return [item[1] for item in chapter_pages_html]


def async_chapter_group(chapters, start):

    links = []
    for i, chapter in enumerate(chapters):
        chapter['number_row'] = start + i + 2
        links.append(
            manga_url + "v"
            + str(chapter["chapter_volume"]) + "/c"
            + chapter['chapter_number'] + "?page=1"
        )
    # print(links)

    chapter_pages = async_js(links)
    chapter_pages = list(map(extract_pages_from_html, chapter_pages))
    # print(chapter_pages)

    # for i in range(len(chapters)):
    chapters_data = [[
        chapters[i]["chapter_id"],
        chapters[i]["chapter_slug"],
        chapters[i]['chapter_name'],
        chapters[i]['chapter_number'],
        chapters[i]['chapter_volume'],
        chapters[i]['number_row'],
        collect_img_slug(chapter_pages[i]),
        ]
        for i in range(len(chapters))
        ]
    set_chapters(chapters_data)


def chapter_group(chapters, start):

    chapter_list = []
    for i, chapter in enumerate(chapters):
        chapter['number_row'] = start + i + 2
        chapter['url'] = (
                manga_url + "v"
                + str(chapter["chapter_volume"]) + "/c"
                + chapter['chapter_number'] + "?page=1")
        chapter = info_chapter(chapter, True)
        chapter_list.append([
            chapter["chapter_id"],
            chapter["chapter_slug"],
            chapter['chapter_name'],
            chapter['chapter_number'],
            chapter['chapter_volume'],
            chapter['number_row'],
            chapter['pages'],
        ])
        # print(chapter_list[i])
    set_chapters(chapter_list)
    print(chapter_list[0][5], chapter_list[-1][5],)


def split_chapters(chapters, start, stop):
    chunk_size = 50
    chapters_list = split_list(chapters[start:stop], chunk_size)

    for chapters in chapters_list:
        start_time = time.time()
        # chapter_group(chapters, start)
        async_chapter_group(chapters, start)
        start += chunk_size
        finish_time = time.time() - start_time
        print(f"\n\n {chunk_size} ta uchun ketgan vaqt: {finish_time} s")


def set_manga(manga_slug, count=None):

    global manga_url
    manga_url = mangaurl(manga_slug)

    chapters, manga = manga_info(manga_slug)
    if not chapters:
        return

    start = len(get_chapters())

    if not count:
        stop = len(chapters) + 10 # 10 ni shunchaki qo'shib qo'ydim
    else:
        stop = start + count

    chapters.reverse()
    split_chapters(chapters, start, stop)
    if not count:
        update_status(manga[0], (6, "completed"))


def list_page(page):
    driver.execute_script(fetch_list_manga + f"top_manga_list({page})")
    items = None
    for i in range(30):
        time.sleep(0.2)
        items = driver.execute_script("return document.rrd;")
        if items:
            break
    manga_list = items.get("items").get("data")

    print(json.dumps(manga_list[:10]))
    # for manga in manga_list:
    #     print(manga['rus_name'])
    #     set_data(manga)


def set_manga_list():
    driver.get("https://mangalib.me/manga-list")
    for i in range(1, 10):
        list_page(i)
        break


def download_list(manga_list=None, count=None):

    if not manga_list:
        manga_list = get_manga_list()
        # manga_list = manga_list[13:]
        manga_list = list(filter(lambda manga: (manga[5] != "completed" and manga[5] != "abandoned"), manga_list))

    if count:
        manga_list = manga_list[:count]
    for i, manga in enumerate(manga_list):
        set_manga(manga[1])
        # break

def main():
    # download_list()
    # manga_slug = "wu-dao-du-zun"
    # set_manga(manga_slug,)
    set_manga_list()


if __name__ == "__main__":
    try:

        start_time = time.time()

        main()

        finish_time = time.time() - start_time
        print(f"\n\n\n yuklab olsih uchun ketgan vaqt: {finish_time} s")

    except Exception as e:
        # time.sleep(10)

        driver.close()
        driver.quit()

        print("\n\nRaised Exception\n\n")
        print(e)

        raise e

    finally:

        driver.close()
        driver.quit()
