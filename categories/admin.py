from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_deleted')
    list_filter = ('is_deleted',)
    prepopulated_fields = {
        'slug': ('name',),
    }
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
