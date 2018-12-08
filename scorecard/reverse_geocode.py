from django.conf import settings
import requests

class ReverseGeocoder(object):
    def lookup(self, longitude, latitude):
        pass

class MapIt(ReverseGeocoder):
    def __init__(self, mapit_url, mapit_generation):
        self.mapit_url = mapit_url
        self.mapit_generation = mapit_generation

    def lookup(self, longitude, latitude):
        url = self.mapit_url + '/point/4326/%s,%s?generation=%s' % (longitude, latitude, self.mapit_generation)
        resp = requests.get(url)
        resp.raise_for_status()
        return [
            (feature["codes"]["MDB"], feature["type_name"])
            for feature
            in resp.json().values()
        ]

mapit_lookup = MapIt(settings.MAPIT["url"], settings.MAPIT["generation"])


