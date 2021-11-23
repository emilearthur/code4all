import unittest
from unittest import mock
import requests
from requests.exceptions import ConnectionError
import requests_mock
from request_ import MyBugzilla


class TestBugzilla(unittest.TestCase):
    def test_bug_id(self):
        zilla = MyBugzilla('tarek@mozilla.com', server = 'http://example.com')
        link = zilla.bug_link(23)
        self.assertEqual(link, 'http://example.com/show_bug.cgi?id=23')

    @requests_mock.mock()
    def test_get_new_bugs(self, mocker):
        # mocking request call and sending two bugs.
        bugs = [{'id': 1184528}, {'id': 1184524}]
        mocker.get(requests_mock.ANY, json={'bugs': bugs})
        
        zilla = MyBugzilla('tarek@mozilla.com', server = 'http://example.com')
        bugs = list(zilla.get_new_bugs())
        self.assertEqual(bugs[0]['link'],'http://example.com/show_bug.cgi?id=1184528')
        