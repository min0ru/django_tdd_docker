import pytest
from django.http import Http404
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ListSerializer

from movies.serializers import MovieSerializer
from movies.views import MovieViewSet


def test_add_movie(client, monkeypatch):
    """ Correct POST request. """
    payload = {"title": "The Big Lebowski", "genre": "comedy", "year": "1998"}

    def mock_create(self, payload):
        return "The Big Lebowski"

    monkeypatch.setattr(MovieSerializer, "create", mock_create)
    monkeypatch.setattr(MovieSerializer, "data", payload)

    response = client.post(reverse("movie-list"), payload, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "The Big Lebowski"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": "Interstellar", "year": "2014"},
    ],
)
def test_add_movie_invalid_json(client, payload):
    """ POST movie with invalid json payload. """
    response = client.post(reverse("movie-list"), payload, content="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_single_movie(client, monkeypatch):
    """ Retrieve single movie by it's id. """
    payload = {
        "title": "Fear and Loathing in Las Vegas",
        "genre": "drama",
        "year": "1998",
    }

    def mock_get_object(self):
        return None

    monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)
    monkeypatch.setattr(MovieSerializer, "data", payload)

    response = client.get(reverse("movie-detail", args=[1]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Fear and Loathing in Las Vegas"


def test_get_single_movie_incorrect_id(client):
    """ Retrieve movie with incorrect id. """
    response = client.get(reverse("movie-detail", args=["bad_movie_id"]))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_single_movie_not_exist(client, monkeypatch):
    """ Retrieve non-existing movie. """

    def mock_get_object(self):
        raise Http404

    monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)

    response = client.get(reverse("movie-detail", args=[9000]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_movies(client, monkeypatch):
    """ Retrieve full list of movies. """
    payload = [
        {"title": "Fear and Loathing in Las Vegas", "genre": "drama", "year": "1998"},
        {
            "title": "Star Wars: Episode II - Attack of the Clones",
            "genre": "drama",
            "year": "2002",
        },
    ]

    monkeypatch.setattr(ListSerializer, "data", payload)

    response = client.get(reverse("movie-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["title"] == "Fear and Loathing in Las Vegas"
    assert response.data[1]["title"] == "Star Wars: Episode II - Attack of the Clones"


def test_remove_movie(client, monkeypatch):
    """ Delete movie. """

    def mock_get_object(self):
        class Movie:
            def delete(self):
                pass

        return Movie()

    monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)

    response = client.delete(reverse("movie-detail", args=[1]))

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_remove_movie_incorrect_id(client, monkeypatch):
    """ Try to remove movie using incorrect id. """

    def mock_get_object(self):
        raise Http404

    monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)

    response = client.delete(reverse("movie-detail", args=[9000]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_movie(client, monkeypatch):
    """ Create movie, update with PUT, check returned info, check updated info with client. """
    payload = {"title": "Fear and Loathing in Las Vegas", "genre": "drama", "year": "1998"}

    def mock_get_object(self):
        return payload

    def mock_perform_update(self, serializer):
        pass

    monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)
    monkeypatch.setattr(MovieViewSet, "perform_update", mock_perform_update)

    response = client.put(
        reverse("movie-detail", args=[1]), payload, content_type="application/json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == payload["title"]
    assert response.data["year"] == payload["year"]


def test_update_movie_incorrect_id(client, monkeypatch):
    """ Request movie update with incorrect id. Check that response is 404 Not Found. """

    def mock_get_object(self):
        raise Http404

    monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)

    response = client.put(reverse("movie-detail", args=[1]), {}, content_type="application/json")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "payload, status_code",
    [
        [{}, 400],
        [{"title": "Fear and Loathing in Las Vegas", "year": 1998}, 400],
    ],
)
def test_update_movie_invalid_json_keys(client, monkeypatch, payload, status_code):
    """ Try to update movie with json that lacks one of required fields. Should return 400. """

    def mock_get_object(self):
        return payload

    monkeypatch.setattr(MovieViewSet, "get_object", mock_get_object)

    response = client.put(
        reverse("movie-detail", args=[1]), payload, content_type="application/json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
