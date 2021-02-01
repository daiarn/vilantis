from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from vilantis.models import ShortURL, Statistics
from vilantis.utils import MD5Strategy, SHA256Strategy, RandomStrategy


def index(request):
    context = {
        "title": _("URL shortener"),
        "main_text": _("Hello world")
    }
    return render(request, 'index.html', context)


def _is_short_url_valid(url):
    return not ShortURL.objects.filter(short_url=url).exists()


def shorten_url(request):
    is_valid = False
    user_url = request.POST.get("url", None)
    algorithm = request.POST.get("algorithm", None)
    if user_url is None or algorithm is None:
        index(request)
    if algorithm == "md5":
        strategy = MD5Strategy()
    elif algorithm == "sha256":
        strategy = SHA256Strategy()
    else:
        strategy = RandomStrategy()

    short_url = ""
    while not is_valid:
        short_url = strategy.get_short_url(user_url)
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
