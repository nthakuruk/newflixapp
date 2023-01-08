db = db.getSiblingDB("movie_db");
db.movie_db.drop();

db.movie_db.insertMany([
    { "name": "videoplayback", "type": "video/mp4", "path_to": "/app/movies/videoplayback.mp4"},
    { "name": "videoplayback_2", "type": "video/mp4", "path_to": "/app/movies/videoplayback_2.mp4"},
    { "name": "videoplayback_3", "type": "video/mp4", "path_to": "/app/movies/videoplayback_3.mp4"}
]);