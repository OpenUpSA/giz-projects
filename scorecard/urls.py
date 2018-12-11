from django.conf.urls import url
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.conf import settings

from django.contrib import admin
import scorecard.views as views
from django.conf.urls.static import static


# This cache is reset on each deployment. Corresponding caching headers are
# sent to the client, too.
CACHE_SECS = 12 * 60 * 60

urlpatterns = [
    url('admin/', admin.site.urls),

    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^sitemap.txt', views.SitemapView.as_view(), name='sitemap'),
    url(r'^api/municipalities', views.MunicipalitiesView.as_view(), name='municipalities'),
    url(r'^api/projects', views.ProjectsView.as_view(), name='projects_api'),
    # e.g. /profiles/province-GT/
    url(
        regex   = '^profiles/(?P<geography_id>\w+-\w+)(-(?P<slug>[\w-]+))?/$',
        view    = cache_page(CACHE_SECS)(views.GeographyDetailView.as_view()),
        kwargs  = {},
        name    = 'geography_detail',
    ),
    url(
        regex   = '^locate/$',
        view    = cache_page(CACHE_SECS)(views.LocateView.as_view()),
        kwargs  = {},
        name    = 'locate',
    ),
    url(
        regex='^robots.txt$',
        view=lambda r: HttpResponse(
            "User-agent: *\nAllow: /\n" +
            "Sitemap: https://municipalmoney.gov.za/sitemap.txt",
            content_type="text/plain"
        )
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
