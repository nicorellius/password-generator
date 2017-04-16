import datetime
import random
import re
import uuid


# get time in format I like
def get_timestamp():
    """
    method to generate timestamp for use in application

    :return timestamp:
    """

    dt = datetime.datetime.now()

    return dt.strftime("%Y-%m-%d %X")


def gen_uid(length=10):
    """
    method to generate random uuid of varying length for application

    :param length: length of uid
    :return uid: formatted string
    """

    # TODO - find one that works in both v2.x/3.x...
    # python 3.x version
    uid = uuid.uuid4()

    tmp_uid = re.sub('-', '', str(uid))

    return ''.join(random.sample(list(tmp_uid), length))

