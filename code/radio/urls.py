from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='radio-index'),
    path('group/<slug:path>/', views.group, name='radio-group'),
    path('play/<slug:path>/', views.play, name='radio-play'),
]
