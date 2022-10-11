from django.urls import path

from . import views

urlpatterns = [
    path(r"wiki/", views.index, name="index"),
    path(r'wiki/create_new_entry', views.create_new_entry, name="create_new_entry"),
    path(r'wiki/result/search_result', views.search_result, name="search_result"),
    path(r"wiki/<str:name>", views.result, name="result"),
    path(r"wiki/create_new_entry", views.create_new_entry, name="create_new_entry"),
    path(r"wiki/result/random_entry", views.random_entry, name="random_entry"),
    path(r"wiki/edit/<str:name>", views.edit, name="edit")
    
]

