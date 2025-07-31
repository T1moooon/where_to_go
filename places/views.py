from django.shortcuts import render
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
