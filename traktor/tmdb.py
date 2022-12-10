import os
import tmdbsimple as tmdb
tmdb.API_KEY = os.environ.get("TMDB_API_KEY", "")


def get_movie_detail(tmdb_id):
    movie = tmdb.Movies(tmdb_id)
    return movie.info(language="zh", append_to_response="images")