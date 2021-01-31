from django.contrib import admin

from vilantis.models import ShortURL, Statistics


class StatisticsInline(admin.TabularInline):
    model = Statistics
    fields = ("time", "ip", "referrer")
    readonly_fields = ("time", "ip", "referrer")
    show_change_link = False
    extra = 0

    def get_min_num(self, request, obj=None, **kwargs):
        extra = 0
        if obj:
            extra = len(obj.statistics_set.all())
        return extra

    def get_max_num(self, request, obj=None, **kwargs):
        return self.get_min_num(request, obj, **kwargs)


class ShortURLAdmin(admin.ModelAdmin):
    fields = ("long_url", "short_url", "clicks", "maximum_clicks", "expiration_time", "is_active")
    readonly_fields = ("long_url", "short_url", "clicks")
    inlines = (StatisticsInline,)


admin.site.register(ShortURL, ShortURLAdmin)
