import random
import string

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import ugettext as _

from vilantis.models import ShortURL


def create_short_url():
    long_url = "https://www.google.com/"
    choices = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(choices) for _ in range(10))
    return ShortURL.objects.create(long_url=long_url, short_url=short_url)


class ShortURLTests(TestCase):

    def setUp(self):
        self.data_random = {"url": "https://www.google.com/", "algorithm": "ran"}
        self.data_md5 = {"url": "https://www.google.com/", "algorithm": "md5"}
        self.data_sha256 = {"url": "https://www.google.com/", "algorithm": "sha256"}

    def tearDown(self):
        ShortURL.objects.all().delete()

    def get_request_results(self, data):
        first_response = self.client.post(path=reverse('shorten_url'), data=data)
        second_response = self.client.post(path=reverse('shorten_url'), data=data)
        return first_response.context["short_url"], second_response.context["short_url"]

    def test_one_url_different_short_url_random(self):
        url1, url2 = self.get_request_results(self.data_random)
        self.assertNotEqual(url1, url2)

    def test_one_url_different_short_url_md5(self):
        url1, url2 = self.get_request_results(self.data_md5)
        self.assertNotEqual(url1, url2)

    def test_one_url_different_short_url_sha256(self):
        url1, url2 = self.get_request_results(self.data_sha256)
        self.assertNotEqual(url1, url2)

    def test_get_long_url_success(self):
        obj = create_short_url()
        path = "/url/{}".format(obj.short_url)
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, obj.long_url)

    def test_get_long_url_not_active(self):
        obj = create_short_url()
        obj.is_active = False
        obj.save()
        path = "/url/{}".format(obj.short_url)
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], _("Link is not active"))

    def test_deactivation(self):
        obj = create_short_url()
        obj.deactivate()
        self.assertEqual(obj.is_active, False)
