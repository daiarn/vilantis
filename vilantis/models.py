from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


class ShortURL(models.Model):
    long_url = models.CharField(verbose_name=_("Long URL"), max_length=255)
    short_url = models.CharField(verbose_name=_("Short URL"), max_length=255)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)
    maximum_clicks = models.IntegerField(
        verbose_name=_("Maximum number of clicks"),
        default=10,
        help_text=_("How many times link can be used before deactivation")
    )
    clicks = models.IntegerField(verbose_name=_("Number of clicks"), default=0)
    expiration_time = models.DateTimeField(verbose_name=_('Expires at'), default=None, null=True, blank=True)

    class Meta:
        verbose_name = _("Short URL")
        verbose_name_plural = _("Short URL's")

    def __str__(self):
        return self.long_url

    @property
    def can_open_link(self):
        return self.clicks < self.maximum_clicks and self.is_active and not self._time_expired()

    def increment_clicks(self):
        self.clicks += 1
        if not self.can_open_link:
            self.is_active = False
        self.save()

    def _time_expired(self):
        if self.expiration_time is None:
            return False
        elif self.expiration_time >= timezone.now():
            return False
        else:
            return True

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()


class Statistics(models.Model):
    short_url = models.ForeignKey(to=ShortURL, verbose_name=_("Url"), on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name=_('Clicked at'), default=timezone.now)
    ip = models.CharField(verbose_name=_('User IP'), max_length=255)
    referrer = models.CharField(verbose_name=_("Referrer URL"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Statistic")
        verbose_name_plural = _("Statistics")

    def __str__(self):
        return _("Statistics of ({})".format(self.short_url))
