
import os

def save_item(item, key):
    if key not in item:
        return ''
    res = item[key]
    if type(res) == str:
        return res
    if type(res) == list and len(res) > 0:
        return str(res[0])
    return ''


def save_artist_title(item):
    res = ''
    if 'artist' in item:
        res += save_item(item, 'artist') + ' - '
    if 'title' in item:
        res += save_item(item, 'title')
    else:
        no_ext = os.path.splitext(item['file'])[0]
        res = os.path.basename(no_ext).replace('_', ' ')
    return res

def save_title(item):
    if 'title' in item:
        res = save_item(item, 'title')
    else:
        no_ext = os.path.splitext(item['file'])[0]
        res = os.path.basename(no_ext).replace('_', ' ')
    return res


def save_album(item):
    if 'album' in item:
        res = save_item(item, 'title')
        if 'date' in item:
            res += ' (' + save_item(item, 'date') + ')'
        return res
    return ''


def save_artist_album_tile(item):
    res = ''
    if 'artist' in item and len(item['artist']) > 0:
        res += save_item(item, 'artist') + ' -- '
    if 'album' in item and len(item['album']) > 0:
        res += save_album(item) + ' -- '
    if 'title' in item and len(item['title']) > 0:
        res += save_item(item, 'title')
    elif 'title' not in item:
        no_ext = os.path.splitext(item['file'])[0]
        res = os.path.basename(no_ext).replace('_', ' ')
    return res
