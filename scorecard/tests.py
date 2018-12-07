from django.test import TestCase
from models import Geography, LocationNotFound
from reverse_geocode import ReverseGeocoder

class DummyGeocoder(ReverseGeocoder):
    def __init__(self, value):
        self.value = value

    def lookup(self, longitude, latitude):
        return self.value

class TestGeography(TestCase):
    def setUp(self):
        self.g = Geography(
            geo_level="municipality",
            geo_code="CPT",
            name="City of Cape Town",
            long_name="City of Cape Town",
            province_name="Western Cape",
            province_code="WC",
            category="A"
        )
        self.g.save()

        self.g2 = Geography(
            geo_level="district",
            geo_code="ABC",
            name="My district",
            long_name="My district",
            province_name="Western Cape",
            province_code="WC",
            category="B"
        )
        self.g2.save()

    def testCategory(self):
        self.assertEquals(self.g.category_name, "metro municipality")
        self.assertEquals(self.g2.category_name, "local municipality")

    def testFind(self):
        geo_code = "CPT"
        geo_level = "municipality"

        val = Geography.find(geo_code, geo_level)
        self.assertEqual(val, self.g)

        try:
            val = Geography.find("Not a muni", geo_level)
            self.fail("Expected LocationNotFound exception to be raised")
        except LocationNotFound:
            pass

        try:
            val = Geography.find(geo_code, "Not a level")
            self.fail("Expected LocationNotFound exception to be raised")
        except LocationNotFound:
            pass
        
    def testGetLocationsFromCoords(self):
        values = [{
            "codes" : { "MDB" : "CPT" },
            "type_name" : "municipality"
        }]
        values = [("CPT", "municipality")]

        dummy_geocoder = DummyGeocoder(values)

        geo = Geography.get_locations_from_coords(dummy_geocoder, 18.4000266, -33.9073491)
        self.assertEqual(len(geo), 1)
        self.assertEqual(geo[0].name, "City of Cape Town")

        values.append(("CPT", "not a municipality"))
        dummy_geocoder = DummyGeocoder(values)

        geo = Geography.get_locations_from_coords(dummy_geocoder, 18.4000266, -33.9073491)
        self.assertEqual(len(geo), 1)

        values.append(("ABC", "district"))

        dummy_geocoder = DummyGeocoder(values)
        geo = Geography.get_locations_from_coords(dummy_geocoder, 18.4000266, -33.9073491)
        self.assertEqual(len(geo), 2)

