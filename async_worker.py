import asyncio
from typing import List, Callable, Any, Tuple


def filtering_to_unique(resluts: list):
    # Create a dictionary to store tuples based on the first item
    unique_tuples_dict = {}

    for idx, val in resluts:
        if idx not in unique_tuples_dict:
            unique_tuples_dict[idx] = (idx, val)
        elif val is not None:
            unique_tuples_dict[idx] = (idx, val)

    # Convert the dictionary values back to a list
    unique_tuples = list(unique_tuples_dict.values())
    unique_list = [t[1] for t in unique_tuples]
    return unique_list

def filtering_type(results: List[Any], value_type: Any, to_type: bool = True) -> List:
    """
    Filter results based on whether they are tuples or not.

    Args:
    - results (List): List of results to filter.
    - to_tuple (bool): Flag indicating whether to filter tuples or non-tuples.

    Returns:
    - List: Filtered list of results.
    """
    if to_type:
        key_func = lambda result: isinstance(result, value_type)
    else:
        key_func = lambda result: not isinstance(result[1], value_type)

    return list(filter(key_func, results))


async def result_links(links: List[Tuple], async_func: Callable) -> Tuple:
    """
    Apply async_func to all links concurrently.

    Args:
    - links (List[Tuple]): List of links to apply async_func to.
    - async_func (Callable): Asynchronous function to apply.

    Returns:
    - List: List of results obtained from applying async_func to links.
    """
    tasks = [async_func(link[1]) for link in links]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def async_loop(links, async_func, try_count, print_error_links, ignor_error, value_type):
    all_results = []
    for i in range(try_count):
        results = await result_links(links, async_func)
        all_results += [
            (links[j][0], result)
            for j, result in enumerate(results)
        ]

        error_links = [
            links[j]
            for j, result in enumerate(results)
            if not isinstance(result, value_type)
        ]

        # print(value_type, type(results[0]), isinstance(results[0], value_type))
        if not error_links:
            break

        links = error_links
        if print_error_links:
            print(links)

    if (try_count - 1 == i) and not ignor_error:
        all_results = filtering_type(all_results, value_type, to_type=False)
        print(all_results)
        raise Exception("\nAn error occurred during asynchronous execution\n")

    return all_results



async def process_links(links: List,
                        async_func: Callable,
                        try_count: int = 10,
                        return_results: bool = True,
                        ignor_error: bool = False,
                        value_type: Any=type(None),
                        only_successful_results: bool = False,
                        print_error_links: bool = False
                        ) -> List:
    """
    Apply async_func to all links, retrying for a certain number of times if errors occur.

    Args:
    - links (List): List of links to apply async_func to.
    - async_func (Callable): Asynchronous function to apply.
    - try_count (int): Number of retry attempts in case of errors.
    - return_results (bool): Flag indicating whether to return results.
    - ignor_error (bool): Flag indicating whether to ignore errors.

    Returns:
    - List: List of results obtained from applying async_func to links.
    """
    if not (isinstance(links, list) or isinstance(links, tuple)):
        links, async_func = async_func, links

    links = [(i, link) for i, link in enumerate(links)]
    all_results = []

    all_results = await async_loop(links, async_func, try_count, print_error_links, ignor_error, value_type)

    if not return_results:
        return
    all_results = sorted(all_results, key=lambda result: result[0])
    all_results = filtering_to_unique(all_results)
    # print(all_results[1])
    if only_successful_results:
        all_results = filtering_type(all_results, value_type)
    return all_results


def sync_process_links(*args, **kwargs) -> List:
    """Synchronous wrapper for process_links."""
    return asyncio.run(process_links(*args, **kwargs))

"""

sync_process_links(list_link, manga_short_info, value_type=dict)

"""