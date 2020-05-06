# radio/views.py

from django.shortcuts import render, redirect


def index(request, mpc):
    context = dict(groups=mpc.list_radio_groups())
    return render(request, 'radio/index.pug', context)


def group(request, path, mpc):
    context = dict(stations=mpc.list_stations(path))
    return render(request, 'radio/group.pug', context)


def play(request, path, mpc):
    mpc.load_radio(path)
    return redirect('index')
