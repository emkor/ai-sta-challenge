import csv
import json
from json import JSONEncoder

from datetime import datetime

from model.ArticleFeatures import ArticleFeatures
from utils.const import FEATURES_DUMP_FILE_NAME, OUTPUT_CSV_FILE
from utils.log_utils import log, seconds_since


class ComplexObjectSerializer(JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        else:
            return o.__dict__


def store_as_csv(testing_article_indexes, testing_article_categories, output_file_name=OUTPUT_CSV_FILE):
    start_time = datetime.utcnow()
    log("Storing prediction results as csv in: {}".format(output_file_name))
    with open(output_file_name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['id', 'specialCoverage'])
        for index, category in zip(testing_article_indexes, testing_article_categories):
            spamwriter.writerow([index, category])
    log("Done storing prediction csv in {}s.".format(seconds_since(start_time)))


def store_features(article_features, features_file_name=FEATURES_DUMP_FILE_NAME):
    """
    :type article_features: list[model.ArticleFeatures.ArticleFeatures]
    :type features_file_name: str
    """
    start_time = datetime.utcnow()
    try:
        with open(features_file_name, mode='w') as output_file:
            json.dump(article_features, output_file, cls=ComplexObjectSerializer)
        log("Done export of {} article's features {}s.".format(len(article_features), seconds_since(start_time)))
    except Exception as e:
        log("Could not export article features data to JSON file: {}. Reason: {}".format(features_file_name, e))


def load_features(features_file_name=FEATURES_DUMP_FILE_NAME):
    """
    :type features_file_name: str
    :rtype: list[model.ArticleFeatures.ArticleFeatures]
    """
    start_time = datetime.utcnow()
    try:
        with open(features_file_name, mode='r') as input_file:
            features_dump = json.load(input_file)
        output_features = []
        for feature in features_dump:
            article_id = int(feature.get("article_id"))
            word_family_index_to_occurences = {}
            for family_index, occurences in feature.get("word_family_index_to_occurences").iteritems():
                if family_index is not None and occurences is not None:
                    word_family_index_to_occurences.update({int(family_index): int(occurences)})
            output_features.append(ArticleFeatures(article_id=article_id,
                                                   word_family_index_to_occurences=word_family_index_to_occurences))
        log("Done import of {} article's features in {}s.".format(len(output_features), seconds_since(start_time)))
        return output_features
    except Exception as e:
        log("Could not import features from JSON file: {}. Reason: {}".format(features_file_name, e))
        return []
