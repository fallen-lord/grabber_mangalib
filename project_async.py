
import aiohttp

from fake_useragent import UserAgent
ua = UserAgent()

async def get_img(link: str) -> tuple:
    async with aiohttp.ClientSession() as session:
        session.headers['Content-Type'] = 'image/jpeg'
        session.headers['Accept-Ranges'] = 'bytes'
        session.headers['User-Agent'] = ua.random

        async with session.get(link) as response:
            result = await response.read()

    return result


async def chapter_img(chapter: list, number_range: int) -> tuple:
    url = chapter[0]
    async with aiohttp.ClientSession() as session:
        session.headers['Content-Type'] = 'image/jpeg'
        session.headers['Accept-Ranges'] = 'bytes'
        session.headers['User-Agent'] = ua.random

        async with session.get(url) as response:
            if response.status == 200:
                result = await response.read()
                return ((number_range, int(chapter[1])),chapter[2], result)
            else:
                print(response.status, response.headers)

from consts import BOT_URL, SOURCE_CHANEL
# a = SOURCE_CHANEL
async def send_main_channel(chapter: list, number_range: int) -> tuple:

    url = BOT_URL + "sendDocument"
    data = aiohttp.FormData()
    data.add_field("chat_id", SOURCE_CHANEL)
    data.add_field('file',
                   chapter[-1],
                   filename=f"Chapter {chapter[1]}.pdf",
                   content_type='application/pdf')
    # data = {"chat_id": SOURCE_CHANEL,
    #         "document": (f"Chapter {chapter[1]}.pdf", chapter[-1])}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                result = await response.json()
                file_id = result['result']['document']['file_id']
                return (number_range, chapter[0], file_id)
            else:
                print(response.status, response.headers)


async def manga_short_info(anime):

    url = "https://mangalib.me/manga-short-info"
    params = {
        "id": anime["id"],
        "slug": anime["slug"],
        "type": "manga",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                result = await response.json()
                return result

async def get_firts_page(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                result = await response.text()
                return result

