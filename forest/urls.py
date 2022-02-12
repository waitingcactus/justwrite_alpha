from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/', views.forest, name='forest'),
    path('<str:username>/add-tree', views.add_tree, name='add-tree'),
]