from rest_framework.viewsets import ModelViewSet

from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
