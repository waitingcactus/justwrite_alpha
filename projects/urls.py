from django.urls import path
from .views import ProjectCreateView, ProjectUpdateView, ProjectDetailView, ProjectDeleteView

from . import views

urlpatterns = [
    path('<str:username>/', views.projects, name='projects'),
    path('<str:username>/new/', ProjectCreateView.as_view(), name='project-create'),
    path('<str:username>/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<str:username>/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('<str:username>/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete')
]