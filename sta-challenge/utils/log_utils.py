from datetime import datetime
from utils.const import MAX_SIZE_OF_DISPLAYING_LIST


class WordIsIgnored(Exception):
    pass


def crop_list_to_max(some_list, length=MAX_SIZE_OF_DISPLAYING_LIST):
    if len(some_list) > length:
        return some_list[:length]
    else:
        return some_list


def log(message):
    """
    :type: str
    """
    print("{} | {}".format(datetime.utcnow(), message))


def seconds_since(start_time):
    """
    :type start_time: datetime
    :rtype: float
    """
    return round((datetime.utcnow() - start_time).total_seconds(), 3)


def percentage(numerator, denominator):
    """
    :type numerator: float | int
    :type denominator: float | int
    :rtype: float
    """
    return round(100. * float(numerator) / float(denominator), 3)
