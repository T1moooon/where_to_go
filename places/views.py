from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from .models import Place


def show_places(request):
    places = Place.objects.all()
    geojson_places = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [float(place.longitude), float(place.latitude)]
                },
                'properties': {
                    'title': place.title,
                    'placeId': place.id,
                    'detailsUrl': reverse('place-json', args=[place.id])
                }
            } for place in places
        ]
    }
    return render(request, 'index.html', {'geojson_places': geojson_places})


def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    imgs = [img.image.url for img in place.images.all().order_by('position')]
    return JsonResponse({
        'title': place.title,
        'imgs': imgs,
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {
            'lat': float(place.latitude),
            'lng': float(place.longitude)
        }
    }, json_dumps_params={'ensure_ascii': False, 'indent': 2})
