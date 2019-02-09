from bs4 import BeautifulSoup
from base64 import b64decode
import json


def list_annotations(emoji):
    def not_tts(type):
        return not type == 'tts'

    found = annotations.find_all('annotation', cp=emoji, type=not_tts)
    if len(found) < 1:
        return []

    return found[0].string.split(' | ')


def write_icon(emoji_name, icon_png):
    f = open(f'images/emoji/{emoji_name}.png', 'wb')
    f.write(icon_png)
    f.close()


def export_emoji(table_row):
    icon_td = table_row.find_all('td', class_='andr alt')
    if len(icon_td) < 1:
        return
    apple_icon = icon_td[0].img
    emoji = apple_icon['alt']
    annotation_list = list_annotations(emoji)
    if len(annotation_list) < 1:
        return

    emoji_name = table_row.find_all('td', class_='name')[0].string.replace(' ', '_')

    maybe_custom = custom_annotations[emoji_name] if emoji_name in custom_annotations else []
    annotation_list = list(set().union(annotation_list, maybe_custom))

    icon_png = b64decode(apple_icon['src'][22:])

    write_icon(emoji_name, icon_png)
    symbols[emoji_name] = emoji
    related[emoji_name] = annotation_list


def get_annotations():
    # wget -O annotations-en.xml https://unicode.org/repos/cldr/tags/latest/common/annotations/en.xml
    # 2019-02-09
    with open('annotations-en.xml') as fp:
        soup = BeautifulSoup(fp, features="lxml")
        return soup


def get_custom_annotations():
    with open('custom_related.json') as fp:
        custom = json.load(fp)

    return custom


annotations = get_annotations()
custom_annotations = get_custom_annotations()
symbols = {}
related = {}


# wget http://unicode.org/emoji/charts/full-emoji-list.html
# 2019-02-09
with open("full-emoji-list.html") as full_list:
    soup = BeautifulSoup(full_list, features="lxml")
    rows = soup.html.body.table.find_all('tr')
    for r in rows:
        if not r.find_all('td'):
            continue
        export_emoji(r)
        # break


with open('symbols.json', 'w') as f:
    json.dump(symbols, f, indent=2, ensure_ascii=False)

with open('related.json', 'w') as f:
    json.dump(related, f, indent=2)

