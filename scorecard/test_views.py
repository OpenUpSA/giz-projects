from django.test import TestCase
from django.test import Client
from django.urls import reverse
        
class TestApi(TestCase):
    fixtures = ['initial_data.json']

class TestProjectsApi(TestApi):

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

class TestMunicipalitiesApi(TestApi):
    def testReverseUrl(self):
        url = reverse("municipalities_api")
        self.assertEquals(url, "/api/municipalities")

    def testProjectsApi(self):
        url = reverse("municipalities_api")
        c = Client()
        response = c.get(url)
        self.assertEquals(response.status_code, 200)

        js = response.json()
        self.assertEquals(type(js), list)
        self.assertGreater(len(js), 0)

class TestProjectDownload(TestCase):
    fixtures = ['initial_data.json']

    def testReverseUrl(self):
        url = reverse("download_projects")
        self.assertEquals(url, "/download-projects")

    def testMimeType(self):
        url = reverse("download_projects")
        c = Client()
        response = c.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("content-type" in response._headers)
        content_type = response._headers["content-type"]
        self.assertTrue("application/vnd.ms-excel" in content_type[1])
        self.assertGreater(len(response.content), 0)
        
