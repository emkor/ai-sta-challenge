from model.word_cache import WordCache
from service.yandex import Yandex
from utils.const import CACHE_DUMP_FILE


def get_word_family_size(family_dump_file_name=CACHE_DUMP_FILE):
    global family_length
    loaded_cache = WordCache(Yandex())
    loaded_cache.load(export_file_name=family_dump_file_name)
    return loaded_cache.get_next_index()
