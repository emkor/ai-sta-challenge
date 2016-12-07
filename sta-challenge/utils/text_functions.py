import unicodedata


def _strip_punctuation(text):
    """
    :type text: unicode
    :rtype: unicode
    """
    punctuation_categoriess = {'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'}
    return ''.join(x for x in text if unicodedata.category(x) not in punctuation_categoriess)


def normalize(text):
    """
    :type: unicode
    :rtype: unicode
    """
    return _strip_punctuation(text).lower()

def strip_tags(text):
    """
    :type text: unicode
    :rtype: unicode
    """
    return text.replace("<b>", "").replace("<pre>", "")

def filter_words_shorter_than(words, length=4):
    """
    :type words: list[unicode]  | unicode
    :type length: int
    :rtype: list[unicode]
    """
    if isinstance(words, list):
        return [word.strip() for word in words if len(word.strip()) >= length]
    else:
        return [word.strip() for word in words.split() if len(word.strip()) >= length]


def filter_nones(values):
    """
    :type: list
    :rtype: list
    """
    return [value for value in values if value is not None]
