import json

from service.article_loader import load_articles
from service.storage import load_features
from utils.const import TRAINING_ARTICLE_ID_TO_CATEGORY, TRAINING_ARTICLES_FILE_NAME, \
    ARTICLE_ID_TO_NORMALIZED_FEATURES_FILE, \
    FEATURES_DUMP_FILE_NAME


def load_article_id_to_cateogory_file(article_id_to_category_file_name=TRAINING_ARTICLE_ID_TO_CATEGORY):
    """
    :type article_id_to_category_file_name: str
    :return: dict[int, int]
    """
    with open(article_id_to_category_file_name, mode='r') as training_article_id_to_category_file:
        training_article_id_to_category = json.load(training_article_id_to_category_file)
    return {int(article_id_unicode): int(category_id) for article_id_unicode, category_id in
            training_article_id_to_category.iteritems()}


def load_article_id_to_normalized_features_file(
        article_id_to_normalized_features_file_name=TRAINING_ARTICLE_ID_TO_CATEGORY):
    """
    :type article_id_to_normalized_features_file_name: str
    :return: dict[int, list[float]]
    """
    with open(article_id_to_normalized_features_file_name, mode='r') as training_article_id_to_category_file:
        article_id_to_normalized_features = json.load(training_article_id_to_category_file)
    return {int(article_id_unicode): normalized_features for article_id_unicode, normalized_features in
            article_id_to_normalized_features.iteritems()}


def build_article_id_to_category_file(output_file_name=TRAINING_ARTICLE_ID_TO_CATEGORY):
    """
    :type output_file_name: str
    :rtype: dict[int, int]
    """
    training_articles = load_articles(TRAINING_ARTICLES_FILE_NAME)
    training_article_id_to_category = {}

    for article in training_articles:
        coverage = article.specialCoverage
        training_article_id_to_category.update({article.id: coverage})

    with open(output_file_name, mode='w') as training_article_id_to_category_file:
        json.dump(training_article_id_to_category, training_article_id_to_category_file)

    return training_article_id_to_category


def build_article_id_to_normalized_features_file(word_families_count, input_file_name=FEATURES_DUMP_FILE_NAME,
                                                 output_file_name=ARTICLE_ID_TO_NORMALIZED_FEATURES_FILE):
    """
    :type word_families_count: int
    :type input_file_name: str
    :type output_file_name: str
    :rtype: dict[int, list[float]]
    """
    loaded_features = load_features(features_file_name=input_file_name)
    article_id_to_normalized_features = {}

    for loaded_feature in loaded_features:
        norm_params = loaded_feature.get_normalized_parameters(word_families_count)
        article_id_to_normalized_features.update({loaded_feature.article_id: norm_params.values()})

    # with open(output_file_name, mode='w') as training_article_id_to_category_file:
    #     json.dump(article_id_to_normalized_features, training_article_id_to_category_file)

    return article_id_to_normalized_features
