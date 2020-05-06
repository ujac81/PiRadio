# music/views.py

from django.shortcuts import render


def index(request, mpc):
    return render(request, 'music/index.pug')
