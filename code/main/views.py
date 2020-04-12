# main/views.py

from django.http import JsonResponse
from django.shortcuts import render


def index(request):

    return render(request, 'main/index.pug', {})


def cmd_ajax(request):
    """POST /ajax/cmd/
    Perform command for MPD (playpause, next, volinc, ....)
    :return: JSON only -- use with ajax!
    """
    action = request.POST.get('action', None)
    ret = dict(test='hallo', action=action)
    res = JsonResponse(ret)  # ensure_thread_mpc().exec_command(request.POST.get('cmd', None)))
    return res
