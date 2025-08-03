from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Place


def show_places(request):
    places = Place.objects.all()
    geojson_places = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(place.longitude), float(place.latitude)]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.id,
                    "detailsUrl": f"/places/{place.id}/json/"
                }
            } for place in places
        ]
    }
    return render(request, 'index.html', {'geojson_places': geojson_places})


def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    imgs = [img.image.url for img in place.images.all().order_by('order')]
    return JsonResponse({
        'title': place.title,
        'imgs': imgs,
        'short_description': place.description_short,
        'long_description': place.description_long,
        'coordinates': {
            'lat': float(place.latitude),
            'lng': float(place.longitude)
        }
    }, json_dumps_params={'ensure_ascii': False, 'indent': 2})
