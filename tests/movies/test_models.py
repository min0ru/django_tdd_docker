import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_movie_model():
    movie = Movie(title="Covid Space Attack 2022", genre="comedy", year="2021")
    movie.save()
    assert movie.title == "Covid Space Attack 2022"
    assert movie.genre == "comedy"
    assert movie.year == "2021"
    assert movie.created_date
    assert movie.updated_date
    assert str(movie) == movie.title
