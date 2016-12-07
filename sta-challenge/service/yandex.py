import json

import requests
from model.word_family import WordFamily
from utils.const import TARGET_ENCODING
from utils.log_utils import log

# YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20161204T113340Z.479c435e51bc5584.edba68f9368a605ac1cbeef52c32178dc34c138f'
# YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20161207T064607Z.80e275a736361e95.2c5f7a5c0c6d74c1114d2e59b5eaee8f9dbd9d17'
# YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20161207T075201Z.c631b9fdd74f1a71.a757d861d55c6f25a700a3c79fba60b7f259d4d7'
# YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20161207T084844Z.c6bedf6e1dc340fb.9eab7e3d88b1345448fe50e7800a57a436d6ed35'
# YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20161207T093154Z.366a2d66822bf85c.01a689d3a7ba9b6dd4e504bf9474016b31d8a4d8'
YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20161207T101750Z.e80f19d9287653b1.aa511cd65310a3af08206a1a458de0b263fc7a92'
YANDEX_TRANSLATE_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

YANDEX_DICTIONARY_URL = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
# YANDEX_DICTIONARY_KEY = 'dict.1.1.20161204T115042Z.535658e9144949a9.c186148706a6a0f439d041fa60028f1f93471b31'
# YANDEX_DICTIONARY_KEY = 'dict.1.1.20161207T064510Z.bff557f26f0f42f4.a2af50d334500a647102af398f4f0c0c25a74c65'
# YANDEX_DICTIONARY_KEY = 'dict.1.1.20161207T080158Z.31cd3f3782788d52.45d910ff8c73197face160bd9ca4a58e03aa204d'
# YANDEX_DICTIONARY_KEY = 'dict.1.1.20161207T084921Z.123e22b8b0d2819a.3a8ed3f9bfda4b352e10a9ccbcbac3067324b0f7'
# YANDEX_DICTIONARY_KEY = 'dict.1.1.20161207T093156Z.f3530655d806d94f.e620f5499b1d396015a27a610221a13c737f814c'
YANDEX_DICTIONARY_KEY = 'dict.1.1.20161207T101647Z.16aa99e396c3c044.7ece61c1d32e0aec5e129b52870913a9d0c9b709'

TO_ENGLISH = 'sl-en'
TO_SLOVENIAN = 'en-sl'
ENGLISH = 'en-en'


class Yandex(object):
    def __init__(self, translate_key=YANDEX_TRANSLATE_KEY, dictionary_key=YANDEX_DICTIONARY_KEY):
        """
        :type translate_key: str
        :type dictionary_key: str
        """
        self.translate_key = translate_key
        self.dictionary_key = dictionary_key

    def to_english(self, slovenian_text):
        """
        :type slovenian_text: unicode
        :rtype: unicode
        """
        data = {
            "text": slovenian_text,
            "format": "plain",
            "lang": TO_ENGLISH,
            "key": self.translate_key
        }
        response = requests.post(url=YANDEX_TRANSLATE_URL, data=data)
        if response.status_code == 200:
            return json.loads(response.content).get("text")[0]
        else:
            log("Could not translate: {} Details: {}".format(response, response.content))
            return None

    def analyze(self, english_word):
        """
        :type english_word: unicode
        :rtype: model.word_family.WordFamily
        """
        return self._call_dictionary_for_word(english_word)

    def _call_dictionary_for_word(self, word):
        """
        :type word: unicode
        :rtype: model.word_family.WordFamily
        """
        data = {
            "text": word.encode(TARGET_ENCODING),
            "lang": ENGLISH,
            "key": self.dictionary_key
        }
        response = requests.post(url=YANDEX_DICTIONARY_URL, data=data)
        if response.status_code == 200:
            words_defs = json.loads(response.content).get("def")
            if words_defs:
                return self.parse_dictionary_response(words_defs)
            else:
                log("Could not parse dictionary response for word: {}. Context: {}".format(word.encode(TARGET_ENCODING),
                                                                                           response.content))
        else:
            log("Could not translate: {} Details: {}".format(response, response.content))
            return None

    def parse_dictionary_response(self, responses_list):
        """
        :type responses_list: list[dict[str, str | dict]]
        :rtype: model.word_family.WordFamily
        """
        response_dict = responses_list[0]
        source_word = response_dict.get("text")
        part_of_speech = response_dict.get("pos")
        synonyms = []
        for synonym_dict in response_dict.get("tr"):
            if synonym_dict.get("pos") == part_of_speech:
                synonyms.append(synonym_dict.get("text"))
        return WordFamily(part_of_speech, synonyms + [source_word])
