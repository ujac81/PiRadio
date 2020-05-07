# radio/views.py

from django.shortcuts import render, redirect


def index(request, mpc):
    context = dict(groups=mpc.list_radio_groups())
    return render(request, 'radio/index.pug', context)


def group(request, path, mpc):
    gname = path.split('__')[1].replace('_', ' ')
    context = dict(stations=mpc.list_stations(path), group=gname)
    return render(request, 'radio/group.pug', context)


def play(request, path, mpc):
    mpc.load_radio(path)
    return redirect('index')
