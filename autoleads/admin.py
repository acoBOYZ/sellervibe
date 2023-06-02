from django.contrib import admin
from .models import App, ProxySetting, AmazonProduct, Webhook
import urllib.parse
from django.urls import reverse
from django.utils.html import format_html

class ProxySettingInline(admin.StackedInline):
    model = ProxySetting
    extra = 1

class AmazonProductInline(admin.StackedInline):
    model = AmazonProduct
    extra = 1

class WebhookInline(admin.StackedInline):
    model = Webhook
    extra = 1

class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'loop_time', 'amazon_base_url', 'compare_value', 'auto_restart_value', 'force_restart_count', 'auto_restart_count', 'view_amazon_products_link')
    search_fields = ('name', 'loop_time', 'amazon_base_url', 'compare_value', 'auto_restart_value', 'force_restart_count', 'auto_restart_count')
    ordering = ('name',)

    inlines = [ProxySettingInline, WebhookInline]

    def view_amazon_products_link(self, obj):
        count = obj.amazon_products.count()
        url = (
            reverse("admin:autoleads_amazonproduct_changelist")
            + "?"
            + urllib.parse.urlencode({"app__id__exact": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Amazon Products</a>', url, count)
    view_amazon_products_link.short_description = 'Amazon Products'


admin.site.register(App, AppAdmin)
admin.site.register(AmazonProduct)
admin.site.register(ProxySetting)
admin.site.register(Webhook)
