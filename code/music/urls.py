from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='music-index'),
    path('browse', views.browse, name='music-browse'),
    path('playlist', views.playlist, name='music-playlist'),
    path('playlists', views.playlists, name='music-playlists'),
    path('search', views.search, name='music-search'),
    path('smart', views.smart, name='music-smart'),
#    path('ajax/cmd/', views.cmd_ajax, name='cmd_ajax'),
]
