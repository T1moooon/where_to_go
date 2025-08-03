from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

from .models import Place, PlaceImage


class PlaceImageInLine(SortableInlineAdminMixin, admin.StackedInline):
    model = PlaceImage
    extra = 3
    fields = ('image', 'previews', 'position')
    readonly_fields = ('previews',)
    ordering = ['position']

    def previews(self, obj):
        if obj.pk and obj.image:
            return format_html(
                "<img src='{}' style='max-width: 300px; max-height: 200px;'/>",
                obj.image.url
            )
        return 'Нет файла'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [PlaceImageInLine]
    list_display = ("title",)
