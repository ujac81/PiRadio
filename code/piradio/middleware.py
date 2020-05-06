
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


class MPCMiddleWare(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        response = view_func(request, *view_args, mpc=ensure_thread_mpc(), **view_kwargs)
        return response
