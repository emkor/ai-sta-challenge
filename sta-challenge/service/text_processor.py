from service.yandex import Yandex
from utils.const import ONLY_WORDS_LONGER_THAN
from utils.text_functions import normalize, filter_words_shorter_than


def chunks(l, n):
    """
    :type l: list | unicode
    :type n: int
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def process_article_to_words(text, yandex_client=Yandex()):
    """
    :type text: unicode
    :type yandex_client: service.yandex.Yandex
    :rtype: list[unicode]
    """
    translated_to_english_list = []
    for text_chunk in chunks(text, 9999):
        english_chunk = yandex_client.to_english(text_chunk)
        translated_to_english_list.append(english_chunk)
    translated_to_english_complete = u"".join(translated_to_english_list)
    normalized_english = normalize(translated_to_english_complete)
    return filter_words_shorter_than(normalized_english.split(), length=ONLY_WORDS_LONGER_THAN)
