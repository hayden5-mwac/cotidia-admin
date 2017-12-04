from django.conf import settings


def admin_settings(request):

    data = {
        "SITE_URL": settings.SITE_URL,
        "SITE_NAME": settings.SITE_NAME,
        "ADMIN_DETAIL_CURRENCY": settings.ADMIN_DETAIL_CURRENCY,
    }

    return data
