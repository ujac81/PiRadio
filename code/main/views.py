# main/views.py

from django.http import JsonResponse
from django.shortcuts import render

from piradio.settings import *


def index(request, mpc):
    context = dict(marquee=mpc.marquee_text())
    return render(request, 'main/index.pug', context)


def cmd_ajax(request, mpc):
    """POST /ajax/cmd/
    Perform command for MPD (playpause, next, volinc, ....)
    :return: JSON only -- use with ajax!
    """
    action = request.POST.get('action', None)
    cmd = request.POST.get('cmd', None)
    if action == 'cmd':
        res = mpc.cmd(request.POST.copy())
    elif action == 'mixer':
        res = dict()
        if cmd == 'vol-status':
            res['Player'] = int(mpc.cmd(dict(cmd='status'))['volume'])
        elif cmd == 'vol-set':
            channel = request.POST.get('channel', None)
            level = int(request.POST.get('value', 0))
            if channel == 'Player':
                mpc.set_volume(level)
    else:
        res = dict(status=False, err_msg='Action not understood: '+action)
    return JsonResponse(res)
