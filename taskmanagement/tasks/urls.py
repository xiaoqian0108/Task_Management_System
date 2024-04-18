from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.JumpToPage.tocreate_event),
    path('create_event/', views.EventManager.create_event),
    path('toupdate_event/', views.JumpToPage.toupdate_event),
    path('update_event/', views.EventManager.update_event),
    path('todelete_event/', views.JumpToPage.todelete_event),
    path('delete_event/', views.EventManager.delete_event),
    path('categories/', views.EventManager.categorized_events),
    path('search/', views.EventManager.search_events),
    path('list_event/', views.EventManager.list_event),
    path('week_events/', views.EventManager.week_events),
    path('event/<int:event_id>/', views.EventManager.update_event_detail, name='event-detail'),
]
