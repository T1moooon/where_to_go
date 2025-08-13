import os
from urllib.parse import urlparse, unquote

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, PlaceImage


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
        raw_place = response.json()

        place, created = Place.objects.get_or_create(
            title=raw_place.get('title', 'Без названия'),
            defaults={
                'short_description': raw_place.get('description_short', ''),
                'long_description': raw_place.get('description_long', ''),
                'longitude': raw_place['coordinates']['lng'],
                'latitude': raw_place['coordinates']['lat']
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создано новое место: {place.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Место уже существует: {place.title}'))

        self.download_images(place, raw_place.get('imgs', []))

    def download_images(self, place, images_urls):
        for position, url in enumerate(images_urls, start=1):
            if 'github.com' in url and '/blob/' in url:
                url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')

            try:
                resp = requests.get(url)
                resp.raise_for_status()
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response else 'no response'
                self.stderr.write(self.style.WARNING(
                    f"[{position}] HTTPError {status} при скачивании {url}"
                ))
                continue
            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.WARNING(
                    f"[{position}] Ошибка при запросе {url}: {e}"
                ))
                continue

            parsed_url = urlparse(url)
            filename = os.path.basename(unquote(parsed_url.path)) or f'image_{position}.jpg'

            img_obj, img_created = PlaceImage.objects.update_or_create(
                place=place,
                position=position,
                defaults={'image': ContentFile(resp.content, name=filename)}
            )

            verb = 'Создана' if img_created else 'Обновлена'
            self.stdout.write(self.style.SUCCESS(f'{verb} картинка #{position}: {filename}'))
