mangalib = None

BASE_WORKSHEET = "MANHUA"

def add_or_get_chapter(worksheet_title):
    # worksheet_title bu manganing slugi

    global chapters, mangalib
    try:
        chapters = mangalib.worksheet(worksheet_title)
    except:

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


def open_sheet(**kwargs):
    import gspread

    from consts import GSHEET_KEY

    gc = gspread.service_account("sources/static_files/credentials.json")

    global mangalib, manga, manga_ids
    mangalib = gc.open_by_key(GSHEET_KEY)

    manga = mangalib.worksheet(BASE_WORKSHEET)
    manga_ids = manga.col_values(1)

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
        upper_or_under('eng'),
        # manga_data['status'],
        # "1",
        "not_started",
        "not_started",
    ]

    manga.append_row(new_manga_data)

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
    manga.update_cell(cell.row, values[0], values[1])

def set_chapters(chapters_list: list):
    start_row = chapters_list[0][5]
    end_row = chapters_list[-1][5]
    range_cells = f"A{start_row}:G{end_row}"
    chapters.update(range_cells, chapters_list)


def get_chapters():
    return chapters.get_all_values()[1:]


def add_file_id(chapter, file_id):
    chapters.update_cell(chapter[5], 6, file_id)

open_sheet()

# if __name__ == "__main__":
#     open_sheet()
#     worksheet = mangalib.worksheet("test")
#     print(worksheet.get_all_values())
    # worksheet.update(range_name='B1', values='Bingo!')
    # worksheet.update_cell(1, 1, 'Bingo!')
    # print([1, 2]*10)
    # worksheet.update(range_name=([1, 3, 26, 3], [9, 6]*13, ))
    # worksheet.update('A1:B2', [[1, 2], [3, 4]])
