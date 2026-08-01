from django.contrib import admin
from .models import *


@admin.register(Religion)
class ReligionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-id',)
    search_fields = ('name',)
    list_per_page=10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-id',)
    search_fields = ('name',)
    list_per_page=10


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-id',)
    search_fields = ('name',)
    list_per_page=10


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-id',)
    search_fields = ('name',)
    list_per_page=10
