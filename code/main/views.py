# main/views.py

from django.http import JsonResponse
from django.shortcuts import render

from mpc.mpc import MPC


# Store MPC client instances per worker in global variable.
# This is usually not recommended, but we know what we are doing.
# In uwsgi mode 5 (or such) workers will be spawned and each one
# should create its own MPC instance and keep it alive for faster access.
# Otherwise a new MPC instance and connection to MPD would be necessary
# upon every single AJAX call. This is bad for performance.
mpc_instances = None


def ensure_thread_mpc():
    """Check if current worker has an MPC instance and create one.

    :return: per worker MPC instance
    """
    global mpc_instances
    try:
        import uwsgi
    except ImportError:
        # If we are not in uwsgi mode, just return an MPC instance.
        if not mpc_instances:
            mpc_instances = MPC()
        return mpc_instances

    if mpc_instances is None:
        # Note: it is not necessary to use a dict here as the
        # mpc_instance variable will be unique per worker, but it looks nicer
        # this way.
        mpc_instances = {}

    worker_id = uwsgi.worker_id()
    if worker_id not in mpc_instances:
        # See comment above about per worker dict.
        mpc_instances[worker_id] = MPC()  # per worker MPC instance

    return mpc_instances[worker_id]


def index(request):
    return render(request, 'main/index.pug', {})


def cmd_ajax(request):
    """POST /ajax/cmd/
    Perform command for MPD (playpause, next, volinc, ....)
    :return: JSON only -- use with ajax!
    """
    action = request.POST.get('action', None)
    if action == 'cmd':
        res = ensure_thread_mpc().cmd(request.POST.copy())
    else:
        res = dict(status=False, err_msg='Action not understood: '+action)
    return JsonResponse(res)
