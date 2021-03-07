from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateTimeField, Model


class CustomUser(AbstractUser):
    pass


class Movie(Model):
    title = CharField(max_length=255)
    genre = CharField(max_length=255)
    year = CharField(max_length=255)
    created_date = DateTimeField(auto_now_add=True)
    updated_date = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
