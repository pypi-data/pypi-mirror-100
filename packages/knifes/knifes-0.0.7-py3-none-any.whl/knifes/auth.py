from django.core.cache import cache
from django.conf import settings
from . import digests
import time
import pickle
import threading


def make_token(token_info, token_expire_time):
    token = digests.md5(str(threading.current_thread().ident) + str(time.time()))
    cache.set(settings.TOKEN_KEY + token, pickle.dumps(token_info), timeout=token_expire_time)
    return token


def update_token(token, token_info, token_expire_time):
    cache.set(settings.TOKEN_KEY + token, pickle.dumps(token_info), timeout=token_expire_time)
    return token


def delete_token(token):
    cache.delete(settings.TOKEN_KEY + token)

