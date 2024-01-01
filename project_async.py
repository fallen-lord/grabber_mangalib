
import aiohttp

from fake_useragent import UserAgent
ua = UserAgent()

async def get_img(link: str, number_page: int) -> tuple:
    async with aiohttp.ClientSession() as session:
        session.headers['Content-Type'] = 'image/jpeg'
        session.headers['Accept-Ranges'] = 'bytes'
        session.headers['User-Agent'] = ua.random


        async with session.get(link) as response:
            result = await response.read()

    return (number_page, result)


async def chapter_img(chapter: list, number_page: int) -> tuple:
    url = chapter[0]
    async with aiohttp.ClientSession() as session:
        session.headers['Content-Type'] = 'image/jpeg'
        session.headers['Accept-Ranges'] = 'bytes'

        async with session.get(url) as response:
            if response.status == 200:
                result = await response.read()
                return ((number_page, int(chapter[1])),chapter[2], result)
            else:
                print(response.status, response.headers)