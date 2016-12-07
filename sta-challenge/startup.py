from datetime import datetime

from service.storage import store_features, load_features
from utils.const import TRAINING_FILE_NAME, CACHE_DUMP_FILE
from utils.log_utils import log, crop_list_to_max, seconds_since
from service.yandex import Yandex
from model.ArticleFeatures import ArticleFeatures
from model.word_cache import WordCache
from service.article_loader import load_articles
from service.text_processor import process_article_to_words
from utils.text_functions import strip_tags, filter_words_shorter_than

articles = load_articles(TRAINING_FILE_NAME)
yandex_client = Yandex()
word_cache = WordCache(yandex_client)
word_cache.load(CACHE_DUMP_FILE)
article_features = load_features()
parsed_features = [article_feature.article_id for article_feature in article_features]

for index, article in enumerate(articles):
    start_time = datetime.utcnow()
    log("Started parsing article #{}: {}...".format(index, article))
    if article.id not in parsed_features:
        article_feature = ArticleFeatures(article.id)
        linked_text_to_translate = strip_tags(article.headline + " " + article.text)
        linked_text_to_translate = filter_words_shorter_than(linked_text_to_translate)
        all_words = process_article_to_words(" ".join(linked_text_to_translate))
        log("Article #{}: {}\nall words ({}): {}...".format(index, article, len(all_words),
                                                            crop_list_to_max(all_words)))
        for word in all_words:
            word_family_index = word_cache.add_word(word)
            if word_family_index is not None:
                article_feature.add_occurence(word_family_index)
        log("Ended parsing #{} article features: {}\narticle analyzed in: {}\n\n".format(index, article_feature,
                                                                                         seconds_since(start_time)))
        word_cache.dump(CACHE_DUMP_FILE)
        store_features(article_features=article_features)
        parsed_features.append(article_feature.article_id)
        article_features.append(article_feature)
    else:
        log("Omitting parsing article #{}: {} - already parsed!".format(index, article))

log("Done!")
