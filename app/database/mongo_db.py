from pymongo import MongoClient


def _get_db():
    client = MongoClient(host='mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource="admin")
    db = client["movie_db"]
    return db


def get_all_movies() -> dict[str, str]:
    db = _get_db()
    return db.movie_db.find()


def add_movie(name: str, type_of_movie_file: str, path_to: str):
    db = _get_db()
    db.movie_db.insert_one({'name': name,
                            'type': type_of_movie_file,
                            'path_to': path_to})


def drop_database():
    db = _get_db()
    # db.movie_db.delete_many({})
    db.movie_db.insert_many([
        {'name': 'videoplayback', 'type': 'video/mp4',
         'path_to': '/app/movies/videoplayback.mp4'},
        {'name': 'videoplayback_2', 'type': 'video/mp4',
         'path_to': '/app/movies/videoplayback_2.mp4'},
        {'name': 'videoplayback_3', 'type': 'video/mp4',
         'path_to': '/app/movies/videoplayback_3.mp4'}
    ])
