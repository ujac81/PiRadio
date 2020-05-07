"""mpc.py -- interface between AJAX request in views and MPDClient.

"""

import logging
import os
import time

from mpd import MPDClient, ConnectionError, CommandError, ProtocolError

from .helpers import *


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
        logging.info('MPD reconnecting...')

        self.connected = False
        self.error = False

        try:
            self.client.disconnect()
        except (ConnectionError, BrokenPipeError, ValueError):
            pass

        for i in range(5):
            try:
                self.client.connect(os.environ.get('MPD_HOST'), int(os.environ.get('MPD_PORT')))
                self.connected = True
            except (ConnectionError, BrokenPipeError, ValueError):
                time.sleep(0.1)
            if self.connected:
                logging.info('MPD reconnected.')
                return True

        self.error = True
        logging.error('reconnect() [FAIL!]')
        return False

    def ensure_connected(self):
        """Make sure we are connected."""
        # Abuse get_status() method which tries to connect up to 5 times.
        self.get_status()

    def get_status(self):
        """Get status dict from mpd.
        If connection error occurred, try to reconnect max 5 times.

        :return: {'audio': '44100:24:2',
                 'bitrate': '320',
                 'consume': '0',
                 'elapsed': '10.203',
                 'mixrampdb': '0.000000',
                 'mixrampdelay': 'nan',
                 'nextsong': '55',
                 'nextsongid': '55',
                 'playlist': '2',
                 'playlistlength': '123',
                 'random': '1',
                 'repeat': '1',
                 'single': '0',
                 'song': '58',
                 'songid': '58',
                 'state': 'pause',
                 'time': '10:191',
                 'volume': '40',
                 'xfade': '0'}

        :return: MPDClient.status()
        """
        res = {'error_str': self.error}
        for i in range(5):
            try:
                res = self.client.status()
                return res
            except (ConnectionError, CommandError, ProtocolError, BrokenPipeError, ValueError):
                self.reconnect()
        res['error_str'] = self.error
        return res

    def get_status_int(self, key, dflt=0):
        """Fetch value from mpd status dict as int,
        fallback to dflt if no such key.
        NOTE: Won't catch failed conversions.
        """
        stat = self.get_status()
        if key in stat:
            return int(stat[key])
        return dflt

    def volume(self):
        """Current volume as int in [0,100]"""
        return self.get_status_int('volume')

    def change_volume(self, amount):
        """Add amount to current volume int [-100, +100]"""
        self.set_volume(self.volume() + amount)

    def set_volume(self, setvol):
        """Set current volume as int in [0,100]"""
        self.ensure_connected()
        vol = setvol
        if vol < 0:
            vol = 0
        if vol > 100:
            vol = 100
        try:
            self.client.setvol(vol)
        except CommandError:
            pass
        return self.volume()

    def get_currentsong(self):
        """Fetch current song dict from mpd.
        Force reconnect if failed.

        :return: {'album': 'Litany',
                 'albumartist': 'Vader',
                 'artist': 'Vader',
                 'date': '2000',
                 'file': 'local/Extreme_Metal/Vader - Litany - 01 - Wings.mp3',
                 'genre': 'Death Metal',
                 'id': '58',
                 'last-modified': '2014-12-10T20:00:58Z',
                 'pos': '58',
                 'time': '191',
                 'title': 'Wings',
                 'track': '1'}
        """
        self.ensure_connected()
        res = self.client.currentsong()
        if len(res) == 0:
            res = {'album': '', 'artist': '', 'title': 'Not Playing!', 'time': 0, 'file': ''}
        return res

    def get_status_data(self):
        """Combined currentsong / status data for AJAX GET or POST on index page

        :return: see generate_status_data()
        """
        status = self.get_status()
        current = self.get_currentsong()
        return self.generate_status_data(status, current)

    @staticmethod
    def generate_status_data(status, current):
        """Combined currentsong / status data

        :return: {title: xxx
                  time: seconds
                  album: xxx
                  artist: xxx
                  date: yyyy
                  id: N
                  elapsed: seconds
                  random: bool
                  repeat: bool
                  volume: percentage
                  state: ['playing', 'stopped', 'paused']
                  playlist: VERSION-NUMBER
                  playlistlength: N
                  file: local/Mp3/...../file.mp3
                  }
        """
        data = {}
        if len(current) == 0:
            current = {'album': '', 'artist': '', 'title': 'Not Playing!', 'time': 0, 'file': ''}
        data['title'] = save_item(current, 'title')
        data['time'] = current['time'] if 'time' in current else 0
        for key in ['album', 'artist', 'date', 'id', 'file']:
            data[key] = save_item(current, key)
        for key in ['elapsed', 'random', 'repeat', 'volume', 'state', 'playlist', 'playlistlength']:
            data[key] = status[key] if key in status else '0'
        data['stream'] = data['file'].startswith('http://') or data['file'].startswith('https://')
        return data

    def cmd(self, data):
        success = True
        err_msg = ''
        cmd = data.get('cmd', None)
        self.ensure_connected()
        try:
            if cmd == 'back':
                self.client.previous()
            elif cmd == 'playpause':
                status = self.get_status()
                if status['state'] == 'play':
                    self.client.pause()
                else:
                    self.client.play()
            elif cmd == 'stop':
                self.client.stop()
            elif cmd == 'next':
                self.client.next()
            elif cmd == 'decvol':
                self.change_volume(-3)
            elif cmd == 'incvol':
                self.change_volume(3)
            elif cmd == 'random':
                rand = self.get_status_int('random')
                self.client.random(1 if rand == 0 else 0)
            elif cmd == 'repeat':
                rep = self.get_status_int('repeat')
                self.client.repeat(1 if rep == 0 else 0)
            elif cmd == 'status':
                pass  # success stays True
            else:
                success = False
        except CommandError:
            success = False
        except ConnectionError:
            success = False

        data = self.get_status_data()
        data['cmd'] = cmd
        data['status'] = success
        data['err_msg'] = err_msg
        return data

    def list_radio_groups(self):
        """" List playlists as groups starting with 'Radio__GROUPNAME__'
        :returns: [['Radio__Heavy_Metal', 'Heavy Metal'], ['Radio__Stations', 'Stations'], ...]
        """
        self.ensure_connected()
        groups = list()
        for x in self.client.listplaylists():
            name = x['playlist']
            if name.startswith('Radio__'):
                path = '__'.join(name.split('__')[0:2])
                groups.append(path)
        return [[x, x.split('__')[1].replace('_', ' ')] for x in sorted(set(groups))]

    def list_stations(self, prefix):
        """ List playlists starting with 'RADIO__prefix__'

        :param prefix: e.g. 'Radio__Stations__'
        :return: [['Radio__Stations__wdr2', 'wdr2'], [....]]
        """
        self.ensure_connected()
        m3us = list()
        for x in self.client.listplaylists():
            name = x['playlist']
            if name.startswith(prefix+'__'):
                m3us.append(name)
        return [[x, x.split('__')[2].replace('_', ' ')] for x in sorted(set(m3us))]

    def load_radio(self, path):
        if self.get_status_data()['stream'] is not True:
            # save current playlist as '__keep.m3u'
            if len(self.client.playlist()) > 0:
                try:
                    self.client.rm('__keep')
                except CommandError:
                    pass
                self.client.save('__keep')
        self.client.clear()
        self.client.load(path)
        self.client.play()

    def marquee_text(self):
        status = self.get_status_data()
        res = ''
        if status['stream'] is True:
            res = 'Radio stream: ' + status['file'] + ' -- '
        res += save_artist_album_tile(status)
        return res
