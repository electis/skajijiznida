from singlemodeladmin import SingleModelAdmin
from django.contrib import admin
from django.apps import apps
from skajijiznida import models

@admin.register(models.Common)
class CommonAdmin(SingleModelAdmin):
    pass

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('image200_tag', 'published', 'ready')
    list_display = ('header', 'date', 'section', 'image50_tag')

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ('image200_tag',)
    list_display = ('article', 'pict', 'image50_tag')
    list_editable = ('pict',)


model_list = apps.get_models()

for model in model_list:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
