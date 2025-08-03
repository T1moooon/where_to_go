from django.contrib import admin
from .models import Place, PlaceImage


class PlaceImageInLine(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'position')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PlaceImageInLine]
