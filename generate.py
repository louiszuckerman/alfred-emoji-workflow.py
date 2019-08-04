from bs4 import BeautifulSoup
from base64 import b64decode
import json


def list_annotations(emoji):
    def not_tts(typ):
        return not typ == 'tts'

    terms = set()
    for anns in {annotations, annotations1}:
        fnd = anns.find_all('annotation', cp=emoji, type=not_tts)
        if len(fnd) > 0:
            terms = terms.union(fnd[0].string.split(' | '))
    return list(terms)


def write_icon(emoji_name, icon_png):
    fi = open(f'images/emoji/{emoji_name}.png', 'wb')
    fi.write(icon_png)
    fi.close()


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

    # icon_png = b64decode(apple_icon['src'][22:])

    # write_icon(emoji_name, icon_png)
    symbols[emoji_name] = emoji
    related[emoji_name] = annotation_list


def get_annotations():
    # wget -O annotations-en.xml https://github.com/unicode-org/cldr/raw/master/common/annotations/en.xml
    # 2019-02-09
    with open('annotations-en.xml') as fp:
        soup = BeautifulSoup(fp, features="lxml")
        return soup


def get_annotations1():
    # wget -O annotations-en1.xml https://github.com/unicode-org/cldr/raw/master/common/annotations/en_001.xml
    # 2019-02-09
    with open('annotations-en1.xml') as fp:
        soup = BeautifulSoup(fp, features="lxml")
        return soup


annotations = get_annotations()
annotations1 = get_annotations1()
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

