from django.urls import path
from .views import ProjectCreateView

from . import views

urlpatterns = [
    path('<str:username>/', views.projects, name='projects'),
    path('<str:username>/new/', ProjectCreateView.as_view(), name='project-create'),
]