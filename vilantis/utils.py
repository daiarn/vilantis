import hashlib
import random
import string
import uuid


def _get_start_index(text):
    if len(text) < 10:
        return None
    return random.choice(range(0, len(text) - 10))


class Strategy(object):
    def get_short_url(self, url):
        raise NotImplementedError


class RandomStrategy(Strategy):
    def get_short_url(self, url):
        choices = string.ascii_letters + string.digits
        return ''.join(random.choice(choices) for _ in range(10))


class MD5Strategy(Strategy):
    def get_short_url(self, url):
        unique_id = uuid.uuid1()
        string_to_hash = str(unique_id) + url
        hash_object = hashlib.md5()
        hash_object.update(string_to_hash.encode())
        result = hash_object.hexdigest()
        start_index = _get_start_index(result)
        if start_index is not None:
            return result[start_index:start_index + 10]
        else:
            return None


class SHA256Strategy(Strategy):
    def get_short_url(self, url):
        unique_id = uuid.uuid1()
        string_to_hash = str(unique_id) + url
        hash_object = hashlib.sha256(string_to_hash.encode())
        result = hash_object.hexdigest()
        start_index = _get_start_index(result)
        if start_index is not None:
            return result[start_index:start_index + 10]
        else:
            return None
