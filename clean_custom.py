import json

custom = json.load(open('custom_related.json', 'r'))
symbols = json.load(open('symbols.json', 'r'))
clean_custom = dict()

for k, v in custom.items():
    if k in symbols:
        clean_custom[k] = list(set(v))
    else:
        if 'our' in k:
            print(f"English! {k} = {', '.join(v)}")

json.dump(clean_custom, open('clean_custom_related.json', 'w'), indent=2)