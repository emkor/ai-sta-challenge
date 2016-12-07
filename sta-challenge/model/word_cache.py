import json
from datetime import datetime
from model.word_family import WordFamily
from service.storage import ComplexObjectSerializer
from utils.const import ACCEPTED_PART_OF_SPEECH, TARGET_ENCODING
from utils.log_utils import log, seconds_since
from utils.text_functions import normalize


class WordCache(object):
    def __init__(self, yandex_client):
        """
        :type yandex_client: service.yandex.Yandex
        """
        self.yandex_client = yandex_client
        self.word_to_family_index = {}
        self.index_to_family = {}
        self.ignored_words = set()

    def add_word(self, word):
        """
        :type word: unicode
        :rtype: int
        """
        if word in self.ignored_words:
            # log("Cache HIT: word {} is known as ignored.".format(word))
            return None

        # case when word is already known to be part of certain family
        word_family_index = self.word_to_family_index.get(normalize(word))
        if word_family_index:
            # log("Cache HIT: word {} is known as member of family {}.".format(word.encode(TARGET_ENCODING),
            #                                                                  word_family_index))
            return word_family_index

        # case when word is not existing in cache yet
        start_time = datetime.utcnow()
        new_family = self.yandex_client.analyze(word)
        if new_family:
            if new_family.part_of_speech in ACCEPTED_PART_OF_SPEECH:
                family_index = self._add_family(new_family)
                # log("Cache MISS: word {} is not known yet, added new {} in {}s.".format(word.encode(TARGET_ENCODING),
                #                                                                         new_family,
                #                                                                         seconds_since(start_time)))
                return family_index
            else:
                # log("Cache MISS: word family {} is not in accepted PoS type, adding to ignored.".format(new_family))
                for synonym in new_family.synonyms:
                    self.ignored_words.add(synonym)
                return None
        else:
            log("Could not create new family, as it is: {}. Adding word: {} to ignored.".format(new_family, word.encode(
                TARGET_ENCODING)))
            self.ignored_words.add(word)
            return None

    def _add_family(self, word_family):
        """
        :type word_family: model.word_family.WordFamily
        :rtype: int
        """
        synonym_to_index_of_existing_family = {}
        for synonym in word_family.synonyms:
            synonym_to_index_of_existing_family.update({synonym: self.word_to_family_index.get(synonym) or None})
        next_index = self.get_next_index()
        self.index_to_family.update({next_index: word_family})
        for word in word_family.synonyms:
            self.word_to_family_index.update({word: next_index})
        return next_index

    def get_next_index(self):
        """
        :rtype: int
        """
        return len(self.index_to_family.keys())

    def dump(self, export_file_name):
        start_time = datetime.utcnow()
        dump = {
            "index_to_family": self.index_to_family,
            "word_to_family_index": self.word_to_family_index,
            "ignored_words": list(self.ignored_words)
        }
        try:
            with open(export_file_name, mode='w') as output_file:
                json.dump(dump, output_file, cls=ComplexObjectSerializer)
            log("Done export of {} families and {} ignored words in {}s.".format(len(self.index_to_family.keys()),
                                                                                 len(self.ignored_words),
                                                                                 seconds_since(start_time)))
        except Exception as e:
            log("Could not export data to JSON file: {}. Reason: {}".format(export_file_name, e))

    def load(self, export_file_name):
        start_time = datetime.utcnow()
        try:
            with open(export_file_name, mode='r') as input_file:
                dump = json.load(input_file)
            self.ignored_words = set(dump.get("ignored_words") or [])
            self.word_to_family_index = dump.get("word_to_family_index") or {}
            index_to_family_dict = dump.get("index_to_family") or {}
            for index, family_dict in index_to_family_dict.iteritems():
                self.index_to_family.update({int(index): WordFamily(part_of_speech=family_dict.get(u"part_of_speech"),
                                                                    synonyms=set(family_dict.get(u"synonyms")))})

            log("Done import of {} families and {} ignored words in {}s.".format(len(self.index_to_family.keys()),
                                                                                 len(self.ignored_words),
                                                                                 seconds_since(start_time)))
        except Exception as e:
            log("Could not import data from JSON file: {}. Reason: {}".format(export_file_name, e))

    def __str__(self):
        return "{} containing {} words and {} ignored words".format(self.__class__.__name__,
                                                                    len(self.index_to_family.keys()),
                                                                    len(self.ignored_words))

    def __repr__(self):
        return self.__str__()
