"""
Unit tests for the gating feature in Studio
"""
from mock import patch
from django.test import TestCase
from opaque_keys.edx.keys import UsageKey
from contentstore.signals import handle_item_deleted


class TestHandleItemDeleted(TestCase):
    """
    Test case for handle_score_changed django signal handler
    """
    def setUp(self):
        super(TestHandleItemDeleted, self).setUp()
        self.test_usage_key = u'block-v1:A+B+C+type@sequential@abcd1234'

    @patch('contentstore.signals.gating_api.set_required_content')
    @patch('contentstore.signals.gating_api.remove_prerequisite')
    def test_handle_item_deleted(self, mock_remove_prereq, mock_set_required):
        """ Test evaluate_prerequisite is called when course.enable_subsection_gating is True """
        handle_item_deleted(usage_key=UsageKey.from_string(self.test_usage_key))
        mock_remove_prereq.assert_called_with(self.test_usage_key)
        mock_set_required.assert_called_with(self.test_usage_key.course_key, self.test_usage_key, None, None)
