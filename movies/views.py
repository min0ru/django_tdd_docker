from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Movie
from .serializers import MovieSerializer


class BaseSerializerListView(APIView):
    serializer = None
    model = None

    def get(self, request):
        objects = self.model.objects.all()
        serializer = self.serializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseDetailView(APIView):
    model = None
    serializer = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer(obj)
        return Response(serializer.data)


class MovieList(BaseSerializerListView):
    model = Movie
    serializer = MovieSerializer


class MovieDetail(BaseDetailView):
    model = Movie
    serializer = MovieSerializer
