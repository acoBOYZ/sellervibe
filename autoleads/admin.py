from django.contrib import admin
from .models import App, AmazonProduct

class AmazonProductInline(admin.TabularInline):
    model = AmazonProduct
    extra = 0

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_by', 'edited_by', 'white_list', 'black_list', 'loop_time', 'amazon_base_url', 'compare_value', 'auto_restart_value', 'force_restart_count', 'auto_restart_count']
    inlines = [AmazonProductInline]
    search_fields = ['name', 'created_by', 'edited_by']

@admin.register(AmazonProduct)
class AmazonProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'app', 'ASIN', 'status']
    search_fields = ['ASIN', 'app__name']