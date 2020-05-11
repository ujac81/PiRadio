
from piradio.settings import *


def mixers(request):
    return dict(mixers=['Player'] + MIXER_CHANNELS)


def view_name(request):
    return dict(url_name=request.resolver_match.url_name)