from django.test import TestCase
from django.conf import settings
from reverse_geocode import ReverseGeocoder, MapIt

class TestMapit(TestCase):
    def testGetLocation(self):
        mapit_lookup = MapIt(settings.MAPIT["url"], settings.MAPIT["generation"])
        geo = mapit_lookup.lookup(18.4000266, -33.9073491)

        self.assertEquals(type(geo), list)
        self.assertEquals(len(geo), 5)

        places = dict([(t[1], t[0]) for t in geo])

        self.assertTrue("SubPlace" in places)
        self.assertEquals(places["SubPlace"], "199037015")

        self.assertTrue("Province" in places)
        self.assertEquals(places["Province"], "WC")

        self.assertTrue("Municipality" in places)
        self.assertEquals(places["Municipality"], "CPT")

        self.assertTrue("Country" in places)
        self.assertEquals(places["Country"], "ZA")
        
