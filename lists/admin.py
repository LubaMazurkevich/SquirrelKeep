from django.contrib import admin
from .models import Category, Tag, List, ListItem

class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 1

class ListAdmin(admin.ModelAdmin):
    inlines = [ListItemInline]
    list_display = ('title', 'category')
    list_filter = ('category', 'tags')
    search_fields = ('title',)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(List, ListAdmin)
admin.site.register(ListItem)
