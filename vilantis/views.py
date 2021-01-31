import hashlib
import random
import string
import uuid
from datetime import datetime

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from vilantis.models import ShortURL, Statistics


def index(request):
    context = {
        "title": _("URL shortener"),
        "main_text": _("Hello world")
    }
    return render(request, 'index.html', context)


def _is_short_url_valid(url):
    return not ShortURL.objects.filter(short_url=url).exists()


def _get_start_index(text):
    if len(text) < 10:
        return None
    return random.choice(range(0, len(text) - 10))


def _random_url():
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for _ in range(10))


def _md5_url(url):
    unique_id = uuid.uuid1()
    string_to_hash = str(unique_id) + url
    hash_object = hashlib.md5()
    hash_object.update(string_to_hash.encode())
    result = hash_object.hexdigest(),
    start_index = _get_start_index(result)
    if start_index is not None:
        return result[start_index:start_index + 10]
    else:
        return None


def _sha256(url):
    unique_id = uuid.uuid1()
    string_to_hash = str(unique_id) + url
    hash_object = hashlib.sha256(string_to_hash.encode())
    result = hash_object.hexdigest()
    start_index = _get_start_index(result)
    if start_index is not None:
        return result[start_index:start_index + 10]
    else:
        return None


def shorten_url(request):
    is_valid = False
    user_url = request.POST.get("url", None)
    if user_url is None:
        index(request)
    short_url = ""
    while not is_valid:
        # short_url = _random_url()
        # short_url = _md5_url(user_url)
        short_url = _sha256(user_url)
        if short_url is None:
            is_valid = False
        else:
            is_valid = _is_short_url_valid(short_url)
    first_part = request.get_host()
    full_url = "{}/url/{}".format(first_part, short_url)
    ShortURL.objects.create(long_url=user_url, short_url=short_url)
    context = {
        "title": _("URL shortener"),
        "main_text": _("Hello world"),
        "short_url": full_url
    }
    return render(request, 'index.html', context)


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _log_statistics(request, obj: ShortURL):
    ip = _get_client_ip(request)
    referrer = request.META.get('HTTP_REFERER')
    Statistics.objects.create(short_url=obj, ip=ip, referrer=referrer)


def long_url(request, short_url):
    obj = get_object_or_404(ShortURL, short_url=short_url)
    if obj.can_open_link:
        obj.increment_clicks()
        _log_statistics(request, obj)
        return HttpResponseRedirect(obj.long_url)
    else:
        obj.deactivate()
        return render(request, 'error.html', {"message": _("Link is not active")})
