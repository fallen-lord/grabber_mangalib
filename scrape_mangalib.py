
import json
import time

from selenium import webdriver
# import undetected_chromedriver as uc

from jscode import *
from mixins import *
from consts import MAIN_DOMAIN
from gsheet import set_data, set_chapter, get_chapters, set_chapters, update_status, get_manga_list, set_list, slugs_and_downloadeds, add_or_get_chapter

options = webdriver.ChromeOptions()
options.add_argument("disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
cService = webdriver.ChromeService(executable_path='sources/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=cService, options=options)

driver.get(MAIN_DOMAIN)
# options = uc.ChromeOptions()
# options.headless = False  # Set headless to False to run in non-headless mode
#
# driver = uc.Chrome(use_subprocess=True, options=options)

freeze = None
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# driver = webdriver.Chrome(options=options)

mangaurl = lambda manga_slug: MAIN_DOMAIN + manga_slug + "/"


def run_js_script(js_script, return_value=True, value_name="document.all_results;", print_script=False):

    if print_script:
        print(js_script)

    driver.execute_script(js_script)

    if not return_value:
        return

    items = None
    for i in range(80):
        time.sleep(0.1)
        items = driver.execute_script("return " + value_name)
        if items:
            break
    return items

def async_worker_in_js(links: list, function_name:str, function_code: str):

    lt = json.dumps(links)
    js_script = function_code + async_worker_in_js_format
    js_script += f"\nlist_link={lt};\n\n"
    js_script += f"sync_process_links(list_link, {function_name});"
    return run_js_script(js_script)

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

    first_page = async_worker_in_js([manga_url],"get_page", get_page)
    if first_page is None:
        update_status(manga_slug, ("downloading", "abandoned"))
        return [], []
    try:
        first_page = first_page[0]['text']
        manga_data = first_page.split("window.__DATA__ = ")
    except:
        print(manga_url)
        return [], []

    manga_data = manga_data[1].split(";\n")[0].strip()
    manga_data = json.loads(manga_data)
    # print(manga_data)

    # driver.get(manga_url)
    # manga_data = driver.execute_script("return window.__DATA__;")

    # if manga_data is None:
    #     update_status(manga_slug, (6, "abandoned"))
    #     return [], []
    chapters_list = greater_team_chapters(manga_data)

    if chapters_list is None:
        update_status(manga_slug, ("downloading", "abandoned"))
        return [], []
    #
    manga = set_data(manga_data['manga'])
    # update_manga_status(manga)

    return chapters_list, manga


def async_js(links: list):

    pages = async_worker_in_js(links, "get_page", get_page)

    return [page['text'] for page in pages]


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
    chunk_size = 60
    chapters_list = split_list(chapters[start:stop], chunk_size)

    for chapters in chapters_list:
        start_time = time.time()
        # chapter_group(chapters, start)
        async_chapter_group(chapters, start)
        start += chunk_size
        finish_time = time.time() - start_time
        print(f"\n\n {chunk_size} ta uchun ketgan vaqt: {finish_time} s")


def set_manga(manga_slug, count=None, index_manga=None):

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
    # print(chapters)
    print(manga_slug)
    # add_or_get_chapter(manga_slug)
    split_chapters(chapters, start, stop)
    if not count:
        update_status(manga[0], ("downloading", "completed"))


def list_page(page):
    chank_size = 100
    print("started")
    js_script = fetch_list_manga + f"top_manga_list({page})"
    items = run_js_script(js_script, value_name="document.rrd;")

    manga_list = items.get("items").get("data")[:chank_size]
    print("got items")

    manga_short_infos = async_worker_in_js(manga_list,
                                           "manga_short_info",
                                           manga_short_info)
    print("got short infos")

    for i, manga in enumerate(manga_list):
        manga.update(manga_short_infos[i])

    set_list(manga_list)

    # for manga in manga_short_infos:
    #     print(manga)
    #     set_data(manga)

def set_manga_list():
    driver.get("https://mangalib.me/manga-list")
    for i in range(1, 20):
        list_page(i)
        # break


def download_list(count=None):

    manga_list = slugs_and_downloadeds()

    for slug, downloading_status, i in manga_list:
        if downloading_status in ["completed", "abandoned"]:
            continue
        i += 2
        set_manga(slug, index_manga=i)
        # break


    if not manga_list:
        manga_list = get_manga_list()
        # manga_list = manga_list[13:]
        manga_list = list(filter(lambda manga: (manga[5] != "completed" and manga[5] != "abandoned"), manga_list))

    if count:
        manga_list = manga_list[:count]
    # for i, manga in enumerate(manga_list):
    #     set_manga(manga[1])
        # break

def main():
    download_list()
    # manga_slug = "wu-dao-du-zun"
    # set_manga(manga_slug="douluo-dalu-ii-jueshi-tangmen")
    # set_manga_list()


if __name__ == "__main__":
    try:

        start_time = time.time()

        main()

        finish_time = time.time() - start_time
        print(f"\n yuklab olsih uchun ketgan vaqt: {finish_time} s")

    except Exception as e:
        # time.sleep(10)

        driver.close()
        driver.quit()

        print("\nRaised Exception\n")
        print(e)

        raise e

    finally:

        driver.close()
        driver.quit()
