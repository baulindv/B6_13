# B6_13

Файл сервера для запуска - album_server.py

Запросить информацию об альбоме можно следующим образом:
http://localhost:8080/albums/Beatles

Добавить информацию об альбоме можно следующим образом:
http -f POST http://localhost:8080/albums year=1990 artist=Ispolnitel genre=Janr album=albom

Год проверяется на int и диапазон значений

Жанр, исполнитель и альбом проверяются на непустые значения
