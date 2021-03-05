import pytest
from django.urls import reverse
from rest_framework import status

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    """ Correct POST request. """
    assert Movie.objects.all().count() == 0
    response = client.post(
        reverse("movie-list"),
        {
            "title": "The Big Lebowski",
            "genre": "comedy",
            "year": "1998",
        },
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Movie.objects.all().count() == 1


@pytest.mark.django_db
def test_add_movie_invalid_json_empty(client):
    """ POST payload is not set. """
    assert Movie.objects.all().count() == 0
    response = client.post(
        reverse("movie-list"), dict(), content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Movie.objects.all().count() == 0


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    """ POST payload is invalid. """
    assert Movie.objects.all().count() == 0
    response = client.post(
        reverse("movie-list"),
        {
            "title": "The Dark Knight Rises",
            "genre": "action",
        },
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Movie.objects.all().count() == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    """ Retrieve single movie by it's id. """
    movie = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    url = reverse("movie-detail", kwargs={"pk": movie.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "The Big Lebowski"


@pytest.mark.django_db
def test_get_single_movie_incorrect_id(client):
    """ Bad movie id. """
    base_url = reverse("movie-list")
    url = f"{base_url}/bad_id/"
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_single_movie_non_exist(client):
    """ Retrieve non-existed movie. """
    assert Movie.objects.all().count() == 0
    url = reverse("movie-detail", kwargs={"pk": 1000})
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    """ Retrieve full list of movies. """
    movie_one = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    movie_two = add_movie(title="Cyberpunk 3020", genre="horror", year="2021")
    response = client.get(reverse("movie-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["title"] == movie_one.title
    assert response.data[1]["title"] == movie_two.title


@pytest.mark.django_db
def test_remove_movie(client, add_movie):
    """ Create movie, get movie, delete movie, check movies list is empty. """
    movie = add_movie(
        title="Fear and Loathing in Las Vegas", genre="drama", year="1998"
    )

    url = reverse("movie-detail", kwargs={"pk": movie.pk})

    response = client.get(url)
    assert response.data["title"] == "Fear and Loathing in Las Vegas"
    assert response.status_code == status.HTTP_200_OK

    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(reverse("movie-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_remove_movie_incorrect_id(client):
    """ Try to remove movie using incorrect id. """
    incorrect_id = 9000
    movie_url = reverse("movie-detail", kwargs={"pk": incorrect_id})
    response = client.delete(movie_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_movie(client, add_movie):
    """ Create movie, update with PUT, check returned info, check updated info with client. """
    movie = add_movie(
        title="Fear and Loathing in Las Vegas", genre="drama", year="1998"
    )
    updated_genre = "comedy"
    url = reverse("movie-detail", kwargs={"pk": movie.pk})
    response = client.put(
        url,
        {
            "title": movie.title,
            "genre": updated_genre,
            "year": movie.year,
        },
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == movie.title
    assert response.data["genre"] == updated_genre
    assert response.data["year"] == movie.year

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["genre"] == updated_genre


@pytest.mark.django_db
def test_update_movie_incorrect_id(client):
    """ Request movie update with incorrect id. Check that response is 404 Not Found. """
    incorrect_id = 95759
    url = reverse("movie-detail", kwargs={"pk": incorrect_id})
    response = client.put(
        url,
        {
            "title": "Tenet",
            "genre": "sci-fi",
            "year": "2020",
        },
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize("payload, status_code", [
    ({}, 400),
    ({"title": "Fear and Loathing in Las Vegas", "year": 1998}, 400),
])
def test_update_movie_invalid_json_keys(client, add_movie, payload, status_code):
    """ Try to update movie with json that lacks one of required fields. Should return 400. """
    movie = add_movie(
        title="Fear and Loathing in Las Vegas", genre="drama", year="1998"
    )
    url = reverse("movie-detail", kwargs={"pk": movie.pk})

    response = client.put(
        url,
        payload,
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
