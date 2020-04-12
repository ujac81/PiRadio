"""mpc.py -- interface between AJAX request in views and MPDClient.

"""

from mpd import MPDClient, ConnectionError, CommandError, ProtocolError


class MPC:
    """MPD Client for all actions in views.py.

    Connect to music player daemon and send/receive data.
    Connects on init, so no need to call reconnect() yourself.
    NOTE: some methods might throw, but this is not too bad for use in django, just reload page.
    """

    def __init__(self):
        """Create MPDClient and connect."""
        self.connected = False
        self.error = False
        self.client = MPDClient()
        self.client.timeout = 10
        self.reconnect()

    def reconnect(self):
        pass

    def cmd(self, data):
        err_msg = ''
        print(data)
        res = dict(cmd='hallo', status=True, err_msg=err_msg)
        return res
