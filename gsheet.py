
import mixins


mangalib = None
worksheets = None

BASE_WORKSHEET = "LIST"

def add_or_get_chapter(worksheet_title):
    # worksheet_title bu manganing slugi

    global chapters, mangalib, worksheets

    if not worksheets:
        worksheets = [ worksheet.title for worksheet in mangalib.worksheets()]


    if worksheet_title in worksheets:
        chapters = mangalib.worksheet(worksheet_title)
    else:

        chapters = mangalib.add_worksheet(title=worksheet_title, rows=1200, cols=7)
        chapters.append_row(
            [
                "id",
                "chapter_slug",
                "chapter_name",
                "chapter_number",
                "chapter_volume",
                "telegram_file_id",
                "pages",
            ]
        )
        worksheets.append(worksheet_title)

    return chapters


def open_sheet(**kwargs):
    import gspread

    from consts import GSHEET_KEY

    gc = gspread.service_account("sources/static_files/credentials.json")

    global mangalib, manga, manga_ids, col_names
    mangalib = gc.open_by_key(GSHEET_KEY)

    manga = mangalib.worksheet(BASE_WORKSHEET)
    manga_ids = manga.col_values(1)
    col_names = manga.row_values(1)

    manga_slug = kwargs.get("manga_slug")
    if manga_slug:
        add_or_get_chapter(manga_slug)


def set_data(manga_data) -> list:

    add_or_get_chapter(manga_data['slug'])

    if str(manga_data["id"]) in manga_ids:
        cell_row = manga_ids.index(str(manga_data["id"])) + 1
        manga_data = manga.row_values(cell_row)
        return manga_data

    upper_or_under = lambda key: manga_data.get(key+'Name') if manga_data.get(key+'Name') else manga_data.get(key+'_name')

    new_manga_data = [

        manga_data['id'],
        manga_data['slug'],
        manga_data['name'],
        upper_or_under("rus"),
        # upper_or_under('eng'),
        # manga_data['type'],
        # manga_data['type_id'],
        # manga_data['status'],
        # "1",
        "not_started",
        "not_started",
    ]



    # manga.append_row(new_manga_data)

    return new_manga_data


def set_chapter(chapter):
    """Chapter malumotlarini gsheet ga joylovchi funksiya"""

    new_chapter = [
        chapter["chapter_id"],
        chapter["chapter_slug"],
        chapter['chapter_name'],
        chapter['chapter_number'],
        chapter['chapter_volume'],
        chapter['number_row'],
        chapter['pages']
    ]

    chapters.append_row(new_chapter)


def update_status(manga_id: str, values: tuple):
    cell = manga.find(manga_id)
    col_number = values[0]
    if isinstance(col_number, str):
        col_number = get_column_number(col_number)
    manga.update_cell(cell.row, col_number, values[1])

def set_chapters(chapters_list: list):
    start_row = chapters_list[0][5]
    end_row = chapters_list[-1][5]
    range_cells = f"A{start_row}:G{end_row}"
    chapters.update(range_cells, chapters_list)


def get_chapters(manga_slug=None):
    if manga_slug:
        add_or_get_chapter(manga_slug)
    return chapters.get_all_values()[1:]


def add_file_id(chapter, file_id):
    if type(chapter) == list:
        chapter = chapter[5]
    chapters.update_cell(chapter, 6, file_id)

def add_files_id(files):
    first_row = files[0][1]
    last_row = len(files) + first_row
    files_id = [file[-1] for file in files]
    range_cells = f"F{first_row}:F{last_row}"
    chapters.update(range_cells, files_id)

open_sheet()

def get_manga_list():
    return manga.get_all_values()[1:]

def set_list(manga_list):

    global manga_ids, manga, col_names
    chunk_size = 10
    col_names = col_names[:26]
    print(col_names)

    manga_list = [
        [
            str(data[col_name])
            for col_name in col_names
        ]
        for data in manga_list
            if not str(data['id']) in manga_ids
    ]
    sub_manga_lists = mixins.split_list(manga_list, chunk_size)

    for manga_lists in sub_manga_lists:

        start_row = len(manga_ids) + 1
        end_row = start_row + chunk_size
        cell_range = f"A{start_row}:Z{end_row}"
        print(cell_range)
        manga.update(cell_range, manga_lists)
        manga_ids += [data[0] for data in manga_lists]

def slugs_and_downloadeds():
    global manga
    slug_number = get_column_number("slug")
    downloading_number = get_column_number("downloading")
    slugs = manga.col_values(slug_number)[1:]
    downloadings = manga.col_values(downloading_number)[1:]
    if len(downloadings) < len(slugs):
        downloadings += [""] * (len(slugs) - len(downloadings))
    # print(downloadings, slugs)
    # print(len(downloadings), len(slugs))
    return ((slug, downloadings[i], i) for i, slug in enumerate(slugs))

def column_by_names(*args):

    global manga
    columns = {
        column_name: manga.col_values(get_column_number(column_name))[1:]
        for column_name in args
    }
    greater_row = 0
    for col in columns.values():
        if greater_row < len(col):
            greater_row = len(col)

    for col in columns.values():
        col += [""] * (greater_row - len(col))
    for i in range(greater_row):
        yield [columns[col][i] for col in args]


def get_column_number(col_name):
    for i, value in enumerate(col_names):
        if value == col_name:
            break
    return i + 1

if __name__ == "__main__":
    # open_sheet()
    # set_list(None)
    # s = column_by_names("slug", "downloading")
    # print(next(s))
    manga_list = column_by_names("slug", "downloading", "sending", "channel_id")

    for manga_data in manga_list:
        if (not manga_data[1] == "completed") or (manga_data[2] == "completed"):
            continue
        print(manga_data)
    # worksheets = mangalib.worksheets()
    # Print the list of worksheet titles
    # worksheets = [worksheet.title for worksheet in mangalib.worksheets()]