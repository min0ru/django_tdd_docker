from rest_framework.serializers import ALL_FIELDS, ModelSerializer

from .models import Movie


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ALL_FIELDS
        read_only_fields = ["id", "created_date", "updated_date"]
