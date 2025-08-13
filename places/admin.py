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
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'image', 'position')
    list_editable = ('position', 'image',)
    search_fields = ('place__title',)
    list_select_related = ('place',)
    autocomplete_fields = ('place',)
