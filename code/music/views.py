# music/views.py

from django.shortcuts import render


def index(request, mpc):
    return render(request, 'music/index.pug')


def browse(request, mpc):
    return render(request, 'music/browse.pug')


def playlist(request, mpc):
    return render(request, 'music/playlist.pug')


def playlists(request, mpc):
    return render(request, 'music/playlists.pug')


def search(request, mpc):
    return render(request, 'music/search.pug')


def smart(request, mpc):
    return render(request, 'music/smart.pug')
