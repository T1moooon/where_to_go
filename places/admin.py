from django.contrib import admin
from django.utils.html import format_html

from .models import Place, PlaceImage


class PlaceImageInLine(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'previews', 'position')
    readonly_fields = ('previews',)

    def previews(self, obj):
        if obj.pk and obj.image:
            return format_html(
                "<img src='{}' style='max-width: 300px; max-height: 200px;'/>",
                obj.image.url
            )
        return 'Нет файла'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PlaceImageInLine]
