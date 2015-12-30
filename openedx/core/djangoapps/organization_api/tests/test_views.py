"""
Tests Organization API.
"""
import json
import unittest
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from oauth2_provider.tests.factories import AccessTokenFactory, ClientFactory

from student.tests.factories import UserFactory
from util import organizations_helpers


@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class OrganizationsAPITests(TestCase):
    """
    Tests for the organizations API endpoints.

    GET /api/organizations/v1/get_organization/org_key/
    """

    def setUp(self):
        """
        Test organizations API.
        """
        super(OrganizationsAPITests, self).setUp()

        self.password = 'password'
        self.organization = {
            'name': 'Test Organization',
            'short_name': 'Orgx',
            'description': 'Testing Organization Helpers Library',
        }
        self.url = reverse(
            'organization_api:get_organization', kwargs={'organization_key': self.organization['short_name']}
        )
        self.user = UserFactory(password=self.password, is_staff=False)

    def test_authentication_required(self):
        """
        Verify the endpoint requires authentication.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_session_auth(self):
        """
        Verify the endpoint supports session authentication.
        """
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(self.url)
        # Assert that org doesn't exist.
        self.assertEqual(response.status_code, 404)

        # Add organization.
        organizations_helpers.add_organization(organization_data=self.organization)

        response = self.client.get(self.url)
        # Assert that user can get organization data.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['organization_name'], self.organization['name'])

    def test_oauth(self):
        """
        Verify the endpoint supports OAuth.
        """
        oauth_client = ClientFactory.create()
        access_token = AccessTokenFactory.create(user=self.user, client=oauth_client).token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token
        }

        response = self.client.get(self.url, **headers)
        # Assert that org doesn't exist.
        self.assertEqual(response.status_code, 404)

        # Add organization.
        organizations_helpers.add_organization(organization_data=self.organization)

        response = self.client.get(self.url, **headers)
        # Assert that user can get organization data.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['organization_name'], self.organization['name'])
