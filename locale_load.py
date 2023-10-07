import locale
import json
import os


def load_language_list(language):
    with open(f"./locale/{language}.json", "r", encoding="utf-8") as f:
        language_list = json.load(f)
    return language_list


class locale_auto:
    def __init__(self, language=None):
        if language in ["Auto", None]:
            language = locale.getdefaultlocale()[
                0
            ]
        if not os.path.exists(f"./locale/{language}.json"):
            language = "en_IN"
        self.language = language
        self.language_map = load_language_list(language)

    def __call__(self, key):
        return self.language_map.get(key, key)

    def print(self):
        print("Use Language:", self.language)
