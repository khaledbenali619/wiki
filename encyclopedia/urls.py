from django.urls import path

from . import views

urlpatterns = [
    path(r"", views.index, name="index"),
    path(r'create_new_entry', views.create_new_entry, name="create_new_entry"),
    path(r'search_result', views.search_result, name="search_result"),
    path(r"/result/<str:name>", views.result, name="result"),
    path(r"create_new_entry", views.create_new_entry, name="create_new_entry"),
    path(r"random_entry", views.random_entry, name="random_entry"),
    path(r"/edit/<str:name>", views.edit, name="edit")
    
]

