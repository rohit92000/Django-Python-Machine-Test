from django.urls import path
from .views import ClientListView, ClientDetailView, ProjectView, UserProjectsView, ProjectDetailView

urlpatterns = [
    path('clients/', ClientListView.as_view()),
    path('clients/<int:id>/', ClientDetailView.as_view()),
    path('projects/', ProjectView.as_view()),
    path('projects/<int:id>/', ProjectDetailView.as_view()),
    path('user/projects/', UserProjectsView.as_view()),
]
