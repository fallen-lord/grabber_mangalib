mangalib = None


def add_or_get_chapter(worksheet_title):
    # worksheet_title bu manganing slugi

    global chapters
    try:
        chapters = mangalib.worksheet(worksheet_title)
    except:

        chapters = mangalib.add_worksheet(title=worksheet_title, rows=500, cols=7)
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

    manga_slug = kwargs.get("manga_slug")
    if type(manga_slug) is not str:
        from consts import MANGA_SLUG
        manga_slug = MANGA_SLUG

    gc = gspread.service_account("sources/static_files/credentials.json")

    global mangalib
    mangalib = gc.open_by_key(GSHEET_KEY)

    add_or_get_chapter(manga_slug)


def set_data(manga_data):
    global mangalib

    if mangalib == None:
        open_sheet(manga_slug=manga_data['slug'])
    else:
        add_or_get_chapter(manga_data['slug'])

    manga = mangalib.worksheet("Manga")
    manga_ids = manga.col_values(4)

    if str(manga_data["id"]) in manga_ids:
        return

    new_manga_data = [

        manga_data['name'],
        manga_data['rusName'],
        manga_data['engName'],
        manga_data['id'],
        manga_data['slug']

    ]

    manga.append_row(new_manga_data)


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


def get_chapters():
    return chapters.get_all_values()[1:]


def add_file_id(chapter, file_id):
    chapters.update_cell(chapter[5], 6, file_id)
