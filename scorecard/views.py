from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.http import Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from wkhtmltopdf.views import PDFResponse
from wkhtmltopdf.utils import wkhtmltopdf

from scorecard.profiles import get_profile
from scorecard.models import Geography, LocationNotFound, Project


class LocateView(TemplateView):
    template_name = 'locate.html'

    def get(self, request, *args, **kwargs):
        self.lat = self.request.GET.get('lat', None)
        self.lon = self.request.GET.get('lon', None)
        self.nope = False

        if self.lat and self.lon:
            place = None
            places = Geography.get_locations_from_coords(latitude=self.lat, longitude=self.lon)

            if places:
                place = places[0]

                # if multiple, prefer the metro/local municipality if available
                if len(places) > 1:
                    places = [p for p in places if p.geo_level == 'municipality']
                    if places:
                        place = places[0]

                return redirect(reverse('geography_detail', kwargs={'geography_id': place.geoid}))
            self.nope = True

        return super(LocateView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        return {
            'nope': self.nope,
            'lat': self.lat,
            'lon': self.lon,
        }


class GeographyDetailView(TemplateView):
    template_name = 'profile/profile_detail.html'

    def dispatch(self, *args, **kwargs):
        self.geo_id = self.kwargs.get('geography_id', None)

        try:
            self.geo_level, self.geo_code = self.geo_id.split('-', 1)
            self.geo = Geography.find(self.geo_code, self.geo_level)
        except (ValueError, LocationNotFound):
            raise Http404

        # check slug
        if kwargs.get('slug') or self.geo.slug:
            if kwargs['slug'] != self.geo.slug:
                kwargs['slug'] = self.geo.slug
                url = '/profiles/%s-%s-%s/' % (self.geo_level, self.geo_code, self.geo.slug)
                return redirect(url, permanent=True)

        return super(GeographyDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        page_context = {}

        profile = get_profile(self.geo)
        page_context.update(profile)

        profile['geography'] = self.geo.as_dict()
        page_context['profile_data'] = profile
        page_context['geography'] = self.geo

        page_context['projects'] = Project.objects.filter(geo=self.geo)

        profile['demarcation']['disestablished_to_geos'] = [
            Geography.objects.filter(geo_code=code).first().as_dict()
            for code in profile['demarcation'].get('disestablished_to', [])]

        profile['demarcation']['established_from_geos'] = [
            Geography.objects.filter(geo_code=code).first().as_dict()
            for code in profile['demarcation'].get('established_from', [])]

        for date in profile['demarcation']['land_gained']:
            for change in date['changes']:
                change['geo'] = Geography.objects.filter(
                    geo_code=change['demarcation_code']).first().as_dict()
        for date in profile['demarcation']['land_lost']:
            for change in date['changes']:
                change['geo'] = Geography.objects.filter(
                    geo_code=change['demarcation_code']).first().as_dict()

        # is this a head-to-head view?
        if 'head2head' in self.request.GET:
            page_context['head2head'] = 'head2head'

        return page_context


class SitemapView(TemplateView):
    template_name = 'sitemap.txt'
    content_type = 'text/plain'

    def get_context_data(self):
        return {
            'geos': Geography.objects.all(),
        }
        
class HomepageView(TemplateView):
    template_name = 'homepage.html'
    content_type = 'text/html'

    def get_context_data(self):
        return {
            'projects': Project.objects.all(),
        }

class MunicipalitiesView(TemplateView):
    content_type = 'text/json'

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        munis = Geography.objects.all()

        return JsonResponse([
            {
                "name" : muni.long_name,
                "url" : "/profiles/%s-%s-%s/" % (muni.geo_level, muni.geo_code, muni.slug),
                "geo_level" : muni.geo_level,
                "id" : muni.slug,
            }
            for muni in munis
        ], safe=False)
