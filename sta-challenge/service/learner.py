from sklearn.neural_network import MLPClassifier
from service.article_loader import load_articles
from service.storage import store_as_csv
from utils.const import ARTICLE_ID_TO_NORMALIZED_FEATURES_FILE, TRAINING_ARTICLE_ID_TO_CATEGORY, \
    TESTING_ARTICLE_ID_TO_NORMALIZED_FEATURES_FILE, FEATURES_DUMP_FILE_NAME, TEST_FEATURES_DUMP_FILE_NAME, \
    CACHE_DUMP_FILE, TESTING_ARTICLES_FILE_NAME, OUTPUT_CSV_FILE
from utils.learn_utils import get_word_family_size
from utils.learner_functions import load_article_id_to_cateogory_file, \
    build_article_id_to_normalized_features_file
from utils.log_utils import log

log("Started learning process")

log("Loading words cache...")
family_length = get_word_family_size(CACHE_DUMP_FILE)

log("Building normalized features for training articles...")
training_article_id_to_norm_features = build_article_id_to_normalized_features_file(family_length,
                                                                                    input_file_name=FEATURES_DUMP_FILE_NAME,
                                                                                    output_file_name=ARTICLE_ID_TO_NORMALIZED_FEATURES_FILE)
log("Loading training data mappings: article id to category...")
training_article_id_to_category = load_article_id_to_cateogory_file(TRAINING_ARTICLE_ID_TO_CATEGORY)
training_article_id_to_category = {article_id: category for article_id, category in
                                   training_article_id_to_category.iteritems() if
                                   article_id in training_article_id_to_norm_features.keys()}

log("Building lists of training values for further learning...")
training_features_list = []
training_categories_list = []
for article_features, features in training_article_id_to_norm_features.iteritems():
    training_features_list.append(features)
    training_categories_list.append(training_article_id_to_category.get(article_features))

log("Learning...")
classifier = MLPClassifier()
classifier.fit(X=training_features_list, y=training_categories_list)

log("Loading testing articles...")
testing_articles = load_articles(TESTING_ARTICLES_FILE_NAME)

log("Building normalized features for testing articles...")
testing_article_id_to_norm_features = build_article_id_to_normalized_features_file(family_length,
                                                                                   input_file_name=TEST_FEATURES_DUMP_FILE_NAME,
                                                                                   output_file_name=TESTING_ARTICLE_ID_TO_NORMALIZED_FEATURES_FILE)
log("Building lists of testing values for prediction...")
testing_article_ids = []
testing_article_features = []
for article in testing_articles:
    article_features = testing_article_id_to_norm_features.get(article.id)
    if article_features:
        testing_article_features.append(article_features)
        testing_article_ids.append(article.id)
    else:
        log("ERROR: Could not find features for article: {}".format(article))

log("Prediction...")
testing_predicted_categories = classifier.predict(X=testing_article_features)

log("Storing results as CSV...")
store_as_csv(testing_article_ids, testing_predicted_categories, output_file_name=OUTPUT_CSV_FILE)

log("Done!")
