
def save_item(item, key):
    if key not in item:
        return ''
    res = item[key]
    if type(res) == str:
        return res
    if type(res) == list and len(res) > 0:
        return res[0]
    return ''
