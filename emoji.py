import json
import sys

with open('symbols.json', 'r') as sym:
    symbols = json.load(sym)

with open('related.json', 'r') as rel:
    related = json.load(rel)

term = sys.argv[1]


def term_matches(item):
    return len([i for i in item if term in i]) > 0


matches = []
for k in related.keys():
    if term_matches(related[k]):
        matches.append(k)


def render_item(k):
    symbol = symbols[k].encode('utf-8')
    return '<item arg="{symbol}" uid="{key}">\n\t<title>{code}</title>\n\t<subtitle>{subtitle}</subtitle>'\
           '\n\t<icon>{icon}</icon>\n</item>'.format(
            key=k,
            symbol=symbol,
            code=':{}:'.format(k),
            subtitle='Copy {} to clipboard'.format(symbol),
            icon='images/{}.png'.format(k)
            )


items = str.join("\n", map(render_item, matches))
print("<?xml version='1.0'?>\n<items>\n{items}\n</items>".format(items=items))
