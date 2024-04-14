from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.EventManager.tocreate_event),
    path('create_event/', views.EventManager.create_event),
    path('toupdate_event/', views.EventManager.toupdate_event),
    path('update_event/', views.EventManager.update_event),
    path('todelete_event/', views.EventManager.todelete_event),
    path('delete_event/', views.EventManager.delete_event),
    path('categories/', views.EventManager.categorized_events),
    path('search/', views.EventManager.search_events),
]
