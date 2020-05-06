
from piradio.settings import *


def mixers(request):
    return dict(mixers=['Player'] + MIXER_CHANNELS)
