
import aiohttp


async def get_img(link, number_page):
    async with aiohttp.ClientSession() as session:
        session.headers['Content-Type'] = 'image/jpeg'
        session.headers['Accept-Ranges'] = 'bytes'

        async with session.get(link) as response:
            result = await response.read()

    return number_page, result
