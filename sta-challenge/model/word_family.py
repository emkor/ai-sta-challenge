class WordFamily(object):
    def __init__(self, part_of_speech, synonyms):
        """
        :type part_of_speech: basestring
        :type synonyms: list[basestring] | set[basestring]
        """
        self.part_of_speech = part_of_speech
        self.synonyms = set(synonyms)

    def contains_word(self, word):
        """
        :type word: unicode
        :rtype: bool
        """
        return self._normalize(word) in self.synonyms

    def add_word(self, word):
        """
        :type word: unicode
        :rtype: model.word_family.WordFamily
        """
        self.synonyms.add(self._normalize(word))
        return self

    def _normalize(self, word):
        """
        :type word: unicode
        :rtype: unicode
        """
        return word.lower().strip()

    def __str__(self):
        return "{} of {}: {}".format(self.__class__.__name__, self.part_of_speech, self.synonyms)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """
        :type other: model.word_family.WordFamily
        :rtype:
        """
        return self.part_of_speech == other.part_of_speech and self.synonyms == other.synonyms

    def __hash__(self):
        return hash(tuple([self.part_of_speech, frozenset(self.synonyms)]))
