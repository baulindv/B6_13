from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

from album import *


@route("/albums/<artist>")
def albums(artist):
    albums_list = album_find(artist)
    # Ошибка, если список пустой
    if not albums_list:
        result = HTTPError(404, f"Альбомов исполнителя {artist} не найдено")
    else:
        # Сформировать HTML документ
        result = f"<!DOCTYPE html>\n" \
                 f"<html lang=\'en\'>\n" \
                 f"<head>\n<title>Albums list</title>\n</head>\n<body>\n" \
                 f"<table><tr><td colspan=\'4\'>Список альбомов исполнителя <b>{artist}</b>. " \
                 f"Всего <b>{len(albums_list)}</b> альбомов:</td></tr>\n" \
                 f"<tr>" \
                 f"<td>№</td><td>Год</td><td>Альбом</td><td>Жанр</td>" \
                 f"</tr>\n"
        for a in albums_list:
            result += f"<tr>" \
                      f"<td>{albums_list.index(a) + 1}</td><td>{a.year}</td><td>{a.album}</td><td>{a.genre}</td>" \
                      f"</tr>\n"
        result += '</table>\n</body>\n</html>'
    return result


def year_check(year, min_year, max_year):
    """
    Проверяет переданный год на int и заданный диапазон.
    В случае успешной проверки возвращает True, иначе - False
    """
    try:
        year = int(year)
    except (ValueError, TypeError):
        return False
    else:
        if int(year) in range(min_year, max_year + 1):
            return True
        else:
            return False


@route('/albums', method='POST')
def save_album():
    # Проверка года на число
    album_year = request.forms.get('year')
    if not year_check(album_year, 1800, 2020):
        return HTTPError(400, "Некорректно указан год")

    # Проверка исполнителя, жанра, альбома на непустое значение
    album_artist = request.forms.get('artist')
    album_genre = request.forms.get('genre')
    album_name = request.forms.get('album')
    for i in [album_artist, album_genre, album_name]:
        if i is None or len(i) == 0:
            return HTTPError(400, "Некорректные параметры жанра, исполнителя или альбома")

    # Проверка на наличие добавляемого альбома в базе
    if is_album_in_db(album_year, album_artist, album_genre, album_name):
        return HTTPError(409, "Добавляемый альбом уже есть в базе")

    # Добавление альбома в базу
    add_album(album_year, album_artist, album_genre, album_name)
    return f'Альбом \'{album_name}\' {album_year} года группы \'{album_artist}\' жанра \'{album_genre}\' добавлен'

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)