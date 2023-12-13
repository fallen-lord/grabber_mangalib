import gspread

from consts import *

gc = gspread.service_account("sources/static_files/credentials.json")

mangalib = gc.open_by_key(GSHEET_KEY)

manga = mangalib.worksheet("Manga")

try:

    chapters = mangalib.worksheet(MANGA_SLUG)

except gspread.exceptions.WorksheetNotFound:

    chapters = mangalib.add_worksheet(title=MANGA_SLUG, rows=500, cols=7)


def add_table_manga(manga_data):
    # if manga_data['slug']

    new_worksheet = mangalib.add_worksheet(

        title=manga_data['slug'],
        rows=manga_data['chapters_count'],
        cols=6

    )

    new_worksheet.append_row(
        ["id",
         "chapter_slug",
         "chapter_name",
         "chapter_number",
         "chapter_volume",
         "pages"]
    )


def set_data(manga_data):
    manga_ids = manga.col_values(4)

    if not str(manga_data["id"]) in manga_ids:
        new_manga_data = [

            manga_data['name'],
            manga_data['rusName'],
            manga_data['engName'],
            manga_data['id'],
            manga_data['slug']

        ]

        manga.append_row(new_manga_data)
        add_table_manga(manga_data)


def set_chapter(chapter):
    chapters = mangalib.worksheet(MANGA_SLUG)

    new_chapter = [

        chapter["chapter_id"],
        chapter["chapter_slug"],
        chapter['chapter_name'],
        chapter['chapter_number'],
        chapter['chapter_volume'],
        chapter['pages']
    ]

    chapters.append_row(new_chapter)


# print(manga.get_all_values())

def get_chapters(manga_slug=MANGA_SLUG):
    chapters = mangalib.worksheet(manga_slug)

    # print(chapters.get_all_values())

    return chapters.get_all_values()[1:]


def add_file_id(chapter, file_id):
    # print(file_id)
    a = chapters.update_cell(chapter[5], 6, file_id)
    # print(a)