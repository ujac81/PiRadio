# radio/views.py

from django.shortcuts import render


def index(request, mpc):
    return render(request, 'radio/index.pug')
