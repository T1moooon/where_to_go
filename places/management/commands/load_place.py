import os
from django.core.management.base import BaseCommand
from places.models import Place, PlaceImage
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse, unquote


class Command(BaseCommand):
    help = "Команда для занесения в бд мест из json"

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='url json файла')

    def handle(self, *args, **options):
        json_url = options['json_url']

        if 'github.com' in json_url and '/blob/' in json_url:
            json_url = json_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')

        response = requests.get(json_url)
        response.raise_for_status()
        place_info = response.json()

        place, created = Place.objects.get_or_create(
            title=place_info.get('title', 'Без названия'),
            defaults={
                'description_short': place_info.get('description_short', ''),
                'description_long': place_info.get('description_long', ''),
                'longitude': place_info['coordinates']['lng'],
                'latitude': place_info['coordinates']['lat']
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создано новое место: {place.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Место уже существует: {place.title}'))

        self.download_images(place, place_info.get('imgs', []))

    def download_images(self, place, images_urls):
        for position, url in enumerate(images_urls, start=1):
            if 'github.com' in url and '/blob/' in url:
                url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')

            resp = requests.get(url)
            resp.raise_for_status()

            parsed = urlparse(url)
            filename = os.path.basename(unquote(parsed.path)) or f'image_{position}.jpg'

            img_obj, img_created = PlaceImage.objects.get_or_create(
                place=place,
                position=position,
                defaults={'image': None}
            )

            img_obj.image.save(filename, ContentFile(resp.content), save=True)

            verb = 'Создана' if img_created else 'Обновлена'
            self.stdout.write(self.style.SUCCESS(f'{verb} картинка #{position}: {filename}'))
