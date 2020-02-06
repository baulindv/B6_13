import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def album_find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def is_album_in_db(year, artist, genre, album):
    """
    Возвращает True, если добавляемый альбом есть в базе, иначе False
    """
    session = connect_db()
    album_query = session.query(Album).filter(Album.year == year,
                                              Album.artist == artist,
                                              Album.genre == genre,
                                              Album.album == album)
    if album_query.count() > 0:
        return True
    return False


def add_album(year, artist, genre, album):
    """
    Добавляет альбом в базу
    """
    album_to_add = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    session = connect_db()
    session.add(album_to_add)
    session.commit()
