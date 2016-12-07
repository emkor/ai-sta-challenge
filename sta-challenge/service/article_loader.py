import json
from datetime import datetime

from model.article import Article, TrainingArticle
from utils.const import TARGET_ENCODING, SOURCE_ENCODING
from utils.log_utils import log, percentage, seconds_since
from utils.text_functions import filter_nones


def article_to_model(article_dict):
    """
    :type article_dict: dict
    :rtype: model.article.Article | model.article.TrainingArticle
    """
    try:
        article_id = int(article_dict.get("id")[0])
        article_categories = article_dict.get("categories")
        article_headline = (article_dict.get("headline")[0]).encode(TARGET_ENCODING)
        article_keywords = [keyword.encode(TARGET_ENCODING) for keyword in article_dict.get("keywords")]
        article_lead = article_dict.get("lede")[0].encode(TARGET_ENCODING)
        if article_dict.get("text"):
            article_text = article_dict.get("text")[0].encode(TARGET_ENCODING)
        else:
            article_text = ''
        article_model = Article(id=article_id, categories=article_categories,
                                headline=article_headline, keywords=article_keywords,
                                lead=article_lead, text=article_text)
        special_coverage_id = article_dict.get("specialCoverage")
        if special_coverage_id:
            return TrainingArticle(specialCoverage=int(special_coverage_id[0]), **article_model.__dict__)
        else:
            return article_model
    except Exception as e:
        log("Exception on parsing article: {}, could not create model. Context: {}".format(e, article_dict.keys()))
        return None


def load_articles(file_name):
    """
    :type file_name: str
    :rtype: list[model.article.Article | model.article.TrainingArticle]
    """
    start_time = datetime.utcnow()
    articles = []

    with open(file_name) as training_file:
        training_file_dicts = json.load(training_file, encoding=SOURCE_ENCODING)

    for training_file_dict in training_file_dicts:
        articles.append(article_to_model(training_file_dict))

    articles = filter_nones(articles)
    log("Loaded {} dicts, translated to {} models ({}%) within {} seconds".format(len(training_file_dicts),
                                                                                  len(articles),
                                                                                  percentage(len(articles),
                                                                                             len(training_file_dicts)),
                                                                                  seconds_since(start_time)))
    return articles
