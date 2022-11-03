from os import listdir
from os.path import isfile, join
import ujson as json
from config import *

languages = {}

def load():
    err = None
    files = [f[:-5] for f in listdir("./lang/") if isfile(join("./lang/", f)) if f.endswith(".json")]
    for i in files:
        f = open(f"./lang/{i}.json")
        try:
            languages[i] = json.loads(f.read())
        except Exception as ex:
            err = (i, ex)
        f.close()
    return err


def check_for_warns():
    warns = []
    if default_language not in languages.keys():
        warns.append(f"default language **{default_language}** not present!")
        return warns
    for key in languages[default_language].keys():
        for lang in languages.keys():
            if lang == default_language:
                continue
            if key not in languages[lang].keys():
                warns.append(f"key **{key}** is not present in language **{lang}**, using default one.")
    for lang in languages.keys():
        if lang == default_language:
            continue
        for key in languages[lang].keys():
            if key not in languages[default_language].keys():
                warns.append(f"key **{key}** is not present in default language **{default_language}**, but exists in language **{lang}**. maybe it's redundant.")
    return warns
