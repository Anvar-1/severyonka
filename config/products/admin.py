from django.contrib import admin
from .models import *


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']

admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Discount)