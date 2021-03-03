from django.urls import path

from .views import MovieList, MovieDetail

urlpatterns = [
    path('api/movies/', MovieList.as_view(), name='api_movies'),
    path('api/movies/<int:pk>/', MovieDetail.as_view(), name='api_movies_pk'),
]