

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

kiril_alp = "йцукенгшщзхъфывапролджэячсмитьбю"

def check_to_latin(img: str) -> bool:
    for i in img:
        if i.lower() in kiril_alp:
            return False
    return True

