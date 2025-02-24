from django.urls import path
from .views import add_post, search

urlpatterns = [
    path("add_post/", add_post, name="add_post"),
    path("search/", search, name="search"),
]
