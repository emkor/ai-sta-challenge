from utils.log_utils import log


class Article(object):
    def __init__(self, id, categories, headline, keywords, lead, text):
        """
        :type id: int
        :type categories: list[unicode]
        :type headline: unicode
        :type keywords: list[unicode]
        :type lead: unicode
        :type text: unicode
        """
        self.text = text
        self.lead = lead
        self.keywords = keywords
        self.headline = headline
        self.categories = categories
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "{} <#{}, headline: {}>".format(self.__class__.__name__, self.id, self.headline)

    def __str__(self):
        return self.__repr__()


class TrainingArticle(Article):
    def __init__(self, id, categories, headline, keywords, lead, text, specialCoverage):
        super(TrainingArticle, self).__init__(id, categories, headline, keywords, lead, text)
        self.specialCoverage = specialCoverage

    def __repr__(self):
        try:
            return "{} <#{}, class: {} headline: {}>".format(self.__class__.__name__, self.id, self.specialCoverage,
                                                             self.headline)
        except Exception as e:
            log("Could not repr training article: {}".format(e))

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
