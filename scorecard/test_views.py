from django.test import TestCase
from django.test import Client
from django.urls import reverse
        
class TestProjectsApi(TestCase):
    fixtures = ['initial_data.json']

    def testReverseUrl(self):
        url = reverse("projects_api")
        self.assertEquals(url, "/api/projects")

    def testProjectsApi(self):
        url = reverse("projects_api")
        c = Client()
        response = c.get(url)
        self.assertEquals(response.status_code, 200)

        js = response.json()
        self.assertEquals(type(js), list)
        self.assertGreater(len(js), 0)

