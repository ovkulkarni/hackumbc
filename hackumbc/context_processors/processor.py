from django.conf import settings


def settings_context(request):
    return {
        "SITE_TITLE": settings.SITE_TITLE
    }
