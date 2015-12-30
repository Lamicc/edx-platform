"""
Organizations API views.
"""
import logging
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework_oauth.authentication import OAuth2Authentication

from util.organizations_helpers import get_organization_by_short_name


log = logging.getLogger(__name__)


class OrganizationsView(APIView):
    """
    View to get organization information.
    """
    authentication_classes = (OAuth2Authentication, SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, organization_key):
        """
        Return organization information related to provided organization key/short_name.
        """
        organization_data = {}
        organization = get_organization_by_short_name(organization_key)
        if organization:
            organization_data['organization_name'] = organization.get('name')
            organization_data['organization_short_name'] = organization.get('short_name')
            organization_data['organization_description'] = organization.get('description')
            organization_logo = organization.get('logo')
            if organization_logo:
                organization_data['organization_logo'] = request.build_absolute_uri(organization_logo.url)

            return Response(organization_data)

        return Response(status=HTTP_404_NOT_FOUND)
