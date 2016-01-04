"""
URLs for the credit app.
"""
from django.conf.urls import patterns, url

from openedx.core.djangoapps.organization_api.api import views


ORGANIZATION_KEY_PATTERN = r'(?P<organization_key>[^/]*)'


urlpatterns = patterns(
    '',
    url(
        r'^v1/organization/{}/$'.format(ORGANIZATION_KEY_PATTERN),
        views.OrganizationsView.as_view(),
        name='get_organization'
    ),
)
