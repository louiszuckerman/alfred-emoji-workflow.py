import json
import os
import sys
import pickle

_COMPARE_STAT_PROPS = {'st_size', 'st_mtime'}
_DATA_SETS = {'custom_related', 'related', 'symbols'}
_STATS = {data_set: os.stat(f'{data_set}.json') for data_set in _DATA_SETS}
_DATA = dict()


def load_index():
    try:
        _DATA['index'] = pickle.load(open('index.p', 'rb'))
    except:
        _DATA['index'] = dict()


def save_index(data_set):
    load_index()
    idx = _DATA['index']
    current = _STATS.get(data_set)
    _DATA['index'].update({data_set: current})
    pickle.dump(idx, open('index.p', 'wb'))


def is_cache_valid(data_set):
    current = _STATS.get(data_set)
    last = _DATA['index'].get(data_set, None)
    return last and all([getattr(last, prop, None) == getattr(current, prop, None) for prop in _COMPARE_STAT_PROPS])


def load_data_set(data_set):
    set_p = f'{data_set}.p'
    if is_cache_valid(data_set):
        _DATA[data_set] = pickle.load(open(set_p, 'rb'))
    else:
        set_json = f'{data_set}.json'
        data = json.load(open(set_json, 'r'))
        pickle.dump(data, open(set_p, 'wb'))
        save_index(data_set)
        _DATA[data_set] = data


def load_data():
    load_index()
    for s in _DATA_SETS:
        load_data_set(s)


def term_matches(strings):
    term = sys.argv[1]
    return any({term in s for s in strings})


def render_item(k):
    symbol = _DATA['symbols'][k].encode('utf-8')
    return '<item arg="{symbol}" uid="{key}">\n\t<title>{code}</title>\n\t<subtitle>{subtitle}</subtitle>'\
           '\n\t<icon>{icon}</icon>\n</item>'.format(
            key=k,
            symbol=symbol,
            code=':{}:'.format(k),
            subtitle='Copy {} to clipboard'.format(symbol),
            icon='images/{}.png'.format(k)
            )


load_data()
matches = {key for key, values in _DATA['related'].items() if term_matches(values)}
matches = list(matches.union({key for key, values in _DATA['custom_related'].items() if term_matches(values)}))
matches.sort(key=lambda item: (item.count('_'), item))
items = str.join("\n", map(render_item, matches))
print("<?xml version='1.0'?>\n<items>\n{items}\n</items>".format(items=items))
