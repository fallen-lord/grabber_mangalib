
import asyncio


def ignor_error(all_results):
    return [
        result
        for result in all_results
        if type(result) == tuple
    ]


async def result_links(links, async_func):
    tasks = [async_func(link, i) for i, link in enumerate(links)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results


async def main_async(links, async_func, try_count=5):
    # async_func funksiyasi tuple tipini qaytarishi kerak

    all_results = []

    for i in range(try_count):

        results = await result_links(links, async_func)
        error_links = []
        all_results += results

        for j, result in enumerate(results):

            if type(result) != tuple:
                error_links.append(links[j])

        if error_links == []:
            break
        links = error_links

        if try_count - i == 1:
            print("\n\n\nAsinxronstda XATOLIK YUZAGA keldi\n\n\n")
            print(results)

    all_results = ignor_error(all_results)
    all_results = sorted(all_results, key=lambda results: result[0])
    # print(all_results)
    return all_results


def main(links, async_func, try_count=5):
    return asyncio.run(main_async(links, async_func, try_count))
