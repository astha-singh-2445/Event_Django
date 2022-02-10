from django.urls import path

from . import views
from .views import EventView

urlpatterns = [
    path('health/', views.health, name='health'),
    path('event/', EventView.as_view(), name="event_post"),
    path('repos/<repo_id>/events/', views.get_event_by_repo_id, name='get_event_by_repo_id'),
    path('users/<user_id>/events/', views.get_event_by_user_id, name='get_event_by_user_id'),
    path('events/<event_id>/', views.get_event_by_event_id, name='get_event_by_event_id')
]
