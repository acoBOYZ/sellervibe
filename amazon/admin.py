from django.contrib import admin
from .models import Product, CategoryTree, Stats, Variations, Offers, DomainExchangeRate, WalmartProduct

class CategoryTreeInline(admin.TabularInline):
    model = CategoryTree
    extra = 0

class StatsInline(admin.TabularInline):
    model = Stats
    extra = 0

class VariationsInline(admin.TabularInline):
    model = Variations
    extra = 0

class OffersInline(admin.TabularInline):
    model = Offers
    extra = 0

class WalmartProductInline(admin.TabularInline):
    model = WalmartProduct
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'asin', 'domainId', 'title', 'updated', 'walmart_updated_status']
    inlines = [CategoryTreeInline, StatsInline, VariationsInline, OffersInline, WalmartProductInline]

    def walmart_updated_status(self, obj):
        return obj.walmart_product.filter(updated=True).exists()
    walmart_updated_status.short_description = 'Walmart Updated'

@admin.register(DomainExchangeRate)
class DomainExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain_code', 'exchange_rate']

@admin.register(WalmartProduct)
class WalmartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'walmartCode', 'pos', 'title', 'priceCurrent', 'updated']
    actions = ['make_updated']

    def make_updated(self, request, queryset):
        queryset.update(updated=True)
    make_updated.short_description = "Mark selected products as updated"
