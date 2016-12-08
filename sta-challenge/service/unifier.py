import json

from datetime import datetime

from model.word_cache import WordCache, similarity, merge_families, update_article_to_features
from service.storage import load_features, store_features
from service.yandex import Yandex
from utils.const import CACHE_DUMP_FILE, FEATURES_DUMP_FILE_NAME, TEST_FEATURES_DUMP_FILE_NAME, UPDATED_DUMP_FILE, \
    UPDATED_TRAINING_FEATURES_DUMP_FILE, UPDATED_TESTING_FEATURES_DUMP_FILE, UPDATED_TESTING_FEATURES_DUMP_FILE2, \
    UPDATED_DUMP_FILE2, UPDATED_TRAINING_FEATURES_DUMP_FILE2
from utils.log_utils import log, seconds_since

SIMILARITIES_FILE_NAME = '/home/mkorzeni/projects/ai-slav-challenge/resources/similarities3.json'


def find_and_store_similar_families(word_cache, filename=SIMILARITIES_FILE_NAME):
    SIMILARITY_THRESHOLD = 0.3

    changes = []
    start_time = datetime.utcnow()
    for outer_index, outer_family in word_cache.index_to_family.iteritems():
        for inner_index, inner_family in word_cache.index_to_family.iteritems():
            if outer_index < inner_index:
                ratio = similarity(outer_family, inner_family)
                if ratio > SIMILARITY_THRESHOLD:
                    log("similarity: {} between (#{}) {} and (#{}) {}".format(round(ratio, 2), inner_index,
                                                                             inner_family.synonyms, outer_index,
                                                                             outer_family.synonyms))
                    changes.append((outer_index, inner_index))
    with open(filename, mode='w') as output_file:
        json.dump(changes, output_file)
    log("Found {} similarities in {}s!".format(len(changes), seconds_since(start_time)))
    return


def load_similarities(filename=SIMILARITIES_FILE_NAME):
    with open(filename, mode='r') as input_file:
        changes = json.load(input_file)
    return changes


yandex_client = Yandex()
word_cache = WordCache(yandex_client)
word_cache.load(UPDATED_DUMP_FILE2)
find_and_store_similar_families(word_cache, filename=SIMILARITIES_FILE_NAME)
# changes = load_similarities(filename=SIMILARITIES_FILE_NAME)
#
# training_features = load_features(features_file_name=UPDATED_TRAINING_FEATURES_DUMP_FILE)
# testing_features = load_features(features_file_name=UPDATED_TESTING_FEATURES_DUMP_FILE)
#
# already_merged = set()
#
# for (outer_index, inner_index) in changes:
#     if outer_index not in already_merged and inner_index not in already_merged:
#         new_cache = merge_families(word_cache, family_to_stay=outer_index, family_to_be_merged=inner_index)
#         if new_cache:
#             already_merged.add(inner_index)
#             already_merged.add(outer_index)
#             word_cache = new_cache
#             training_features = update_article_to_features(old_family_index=inner_index, new_family_index=outer_index,
#                                                            article_feature_list=training_features)
#             testing_features = update_article_to_features(old_family_index=inner_index, new_family_index=outer_index,
#                                                           article_feature_list=testing_features)
#
#
# word_cache.dump(UPDATED_DUMP_FILE2)
# store_features(training_features, UPDATED_TRAINING_FEATURES_DUMP_FILE2)
# store_features(testing_features, UPDATED_TESTING_FEATURES_DUMP_FILE2)
