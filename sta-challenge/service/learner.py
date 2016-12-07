from sklearn.neural_network import MLPClassifier

from model.word_cache import WordCache
from service.yandex import Yandex
from utils.const import TEMPORARY_CACHE_FILE, ARTICLE_ID_TO_NORMALIZED_FEATURES_FILE, TRAINING_ARTICLE_ID_TO_CATEGORY
from utils.learner_functions import load_article_id_to_normalized_features_file, load_article_id_to_cateogory_file, \
    build_article_id_to_normalized_features_file

# loaded_cache = WordCache(Yandex())
# loaded_cache.load(export_file_name=TEMPORARY_CACHE_FILE)
# family_length = loaded_cache.get_next_index()

# build_article_id_to_normalized_features_file(family_length)

article_id_to_normalized_features = load_article_id_to_normalized_features_file(ARTICLE_ID_TO_NORMALIZED_FEATURES_FILE)
article_id_to_category = load_article_id_to_cateogory_file(TRAINING_ARTICLE_ID_TO_CATEGORY)
article_id_to_category = {article_id: category for article_id, category in article_id_to_category.iteritems() if
                          article_id in article_id_to_normalized_features.keys()}
classifier = MLPClassifier()

list_of_features_of_samples = []
list_of_categories = []
for article_id, features in article_id_to_normalized_features.iteritems():
    list_of_features_of_samples.append(features)
    list_of_categories.append(article_id_to_category.get(article_id))

classifier.fit(X=list_of_features_of_samples, y=list_of_categories)
########################
testing_article_indexes = []
testing_data_list_of_features_of_samples = [[]]

testing_predicted_classes = classifier.predict(X=testing_data_list_of_features_of_samples)

pass
