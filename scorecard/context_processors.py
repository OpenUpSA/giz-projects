from django.conf import settings

def google_analytics(request):
    """
    Add the Google Analytics tracking ID and domain to the context for use when
    rendering tracking code.
    """
    ga_id = None
    if not settings.DEBUG:
        ga_id = getattr(settings, 'SCORECARD_GOOGLE_ANALYTICS_ID', None)

    return {'GOOGLE_ANALYTICS_ID': ga_id}

