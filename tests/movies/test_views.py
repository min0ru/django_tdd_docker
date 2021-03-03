import pytest

from django.urls import reverse
from rest_framework import status

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    """ Correct POST request. """
    assert Movie.objects.all().count() == 0
    response = client.post(
        reverse('api_movies'),
        {
            'title': 'The Big Lebowski',
            'genre': 'comedy',
            'year': '1998',
        },
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Movie.objects.all().count() == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    """ POST payload is not set. """
    assert Movie.objects.all().count() == 0
    response = client.post(
        reverse('api_movies'),
        dict(),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Movie.objects.all().count() == 0


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    """ POST payload is invalid. """
    assert Movie.objects.all().count() == 0
    response = client.post(
        reverse('api_movies'),
        {
            'title': 'The Dark Knight Rises',
            'genre': 'action',
        },
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Movie.objects.all().count() == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    """ Retrieve single movie by it's id. """
    movie = add_movie(title='The Big Lebowski', genre='comedy', year='1998')
    url = reverse('api_movies_pk', kwargs={'pk': movie.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'The Big Lebowski'


@pytest.mark.django_db
def test_get_single_movie_incorrect_id(client):
    """ Bad movie id. """
    base_url = reverse('api_movies')
    url = f'{base_url}/bad_id/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_single_movie_non_exist(client):
    """ Retrieve non-existed movie. """
    assert Movie.objects.all().count() == 0
    url = reverse('api_movies_pk', kwargs={'pk': 1000})
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title='The Big Lebowski', genre='comedy', year='1998')
    movie_two = add_movie(title='Cyberpunk 3020', genre='horror', year='2021')
    response = client.get(reverse('api_movies'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['title'] == movie_one.title
    assert response.data[1]['title'] == movie_two.title
