from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import CustomUser, Movie


@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    pass

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'genre', 'year', 'created_date', 'updated_date']
    fields = ['id', 'title', 'genre', 'year', 'created_date', 'updated_date']
    readonly_fields = ['id', 'created_date', 'updated_date']
