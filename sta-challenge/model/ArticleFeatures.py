from utils.log_utils import crop_list_to_max


class ArticleFeatures(object):
    def __init__(self, article_id, word_family_index_to_occurences=None):
        """
        :type article_id: int
        :type word_family_index_to_occurences: dict[id, int]
        """
        self.article_id = article_id
        self.word_family_index_to_occurences = word_family_index_to_occurences or {}

    def get_normalized_parameters(self, word_family_length):
        """
        :type word_family_length: int
        :rtype: dict[id, float]
        """
        total_occurences = float(sum(self.word_family_index_to_occurences.values()))
        normalized_params = {}
        for family_index in xrange(0, word_family_length):
            normalized_params.update(
                {family_index: self.word_family_index_to_occurences.get(family_index) or 0 / total_occurences})

        return normalized_params

    def add_occurence(self, word_family_index):
        """
        :type word_family_index: int
        """
        occurences = self.word_family_index_to_occurences.get(word_family_index) or 0
        self.word_family_index_to_occurences.update({word_family_index: occurences + 1})

    def __str__(self):
        return "{} for #{} word family to occurences: {}".format(self.__class__.__name__, self.article_id,
                                                                 crop_list_to_max(
                                                                     self.word_family_index_to_occurences.values()))

    def __repr__(self):
        return self.__str__()
