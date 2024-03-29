import os
import unittest
from unittest import mock
import datetime

import hatena_blog


def _get_client():
    client = hatena_blog.Client(
        hatena_id="hatena_id",
        blog_id="blog_id",
        api_key="api_key"
    )
    return client


class TestHatenaBlogClient(unittest.TestCase):
    def setUp(self):
        self.client = _get_client()

    def test_client(self):
        self.assertIsInstance(self.client, hatena_blog.Client)

    @mock.patch('hatena_blog.Collection.__init__')
    @mock.patch('requests.Session.get')
    def test_get_collection(self, requests_get, hatena_blog_collection_init):
        requests_get.return_value.status_code = 200
        requests_get.return_value.content = 'xml data'
        hatena_blog_collection_init.return_value = None
        collection = self.client.get_collection()
        self.assertIsInstance(collection, hatena_blog.Collection)
        hatena_blog_collection_init.called_once_with('xml data')

    @mock.patch('hatena_blog.Collection.__init__')
    @mock.patch('requests.Session.get')
    def test_get_collection_by_categories(self, requests_get, hatena_blog_collection_init):
        requests_get.return_value.status_code = 200
        requests_get.return_value.content = 'xml data'
        hatena_blog_collection_init.return_value = None
        category = "category1"
        collection = self.client.get_collection(category=category)
        self.assertIsInstance(collection, hatena_blog.Collection)
        hatena_blog_collection_init.called_once_with('xml data')

    def test_get_entry(self):
        entry_id = "1234567890"
        entry = self.client.get_entry(entry_id)
        self.assertIsInstance(entry, hatena_blog.Entry)
        self.assertEqual(entry.entry_id, entry_id)

    def test_get_entry(self):
        entry = self.client.get_entry()
        self.assertIsInstance(entry, hatena_blog.Entry)

    @mock.patch('requests.get')
    def test_pull_entry(self, requests_get):
        entry_id = "1234567890"
        entry = self.client.get_entry(entry_id)
        self.client.pull_entry(entry)
        requests_get.assert_called_once()

    @mock.patch('requests.post')
    def test_push_entry(self, requests_post):
        entry_id = "1234567890"
        entry = self.client.get_entry(entry_id)
        self.client.push_entry(entry)
        requests_post.assert_called_once()


class TestCollection(unittest.TestCase):
    def setUp(self):
        self.client = _get_client()

    @mock.patch('requests.Session.get')
    def test_collection_entries(self, requests_get):
        """正常系"""
        with open(
                os.path.join(os.path.dirname(__file__),
                'data/collection_case1.xml'), 'r') as f:
            response_data = f.read()
        requests_get.return_value.status_code = 200
        requests_get.return_value.content = response_data

        collection = self.client.get_collection()

        self.assertIsInstance(collection.entries, list)
        self.assertIsInstance(collection.entries[0], hatena_blog.Entry)

    @mock.patch('requests.Session.get')
    def test_collection_entries(self, requests_get):
        """異常系"""
        requests_get.return_value.status_code = 401
        with self.assertRaises(hatena_blog.InvalidRequestsError):
            collection = self.client.get_collection()

    @mock.patch('requests.Session.get')
    def test_collection_public_entries(self, requests_get):
        """正常系"""
        with open(
                os.path.join(os.path.dirname(__file__),
                'data/collection_case1.xml'), 'r') as f:
            response_data = f.read()
        requests_get.return_value.status_code = 200
        requests_get.return_value.content = response_data

        collection = self.client.get_collection()
        entries = collection.public_entries

        self.assertIsInstance(entries, list)
        self.assertIsInstance(entries[0], hatena_blog.Entry)
        self.assertTrue(entries[0].is_public)

    @mock.patch('requests.Session.get')
    def test_collection_draft_entries(self, requests_get):
        """正常系"""
        with open(
                os.path.join(os.path.dirname(__file__),
                'data/collection_case1.xml'), 'r') as f:
            response_data = f.read()
        requests_get.return_value.status_code = 200
        requests_get.return_value.content = response_data

        collection = self.client.get_collection()
        entries = collection.draft_entries

        self.assertIsInstance(entries, list)
        self.assertIsInstance(entries[0], hatena_blog.Entry)
        self.assertFalse(entries[0].is_public)

    @mock.patch('requests.Session.get')
    def test_collection_next(self, requests_get):
        """正常系(次がないケース)"""
        with open(
                os.path.join(os.path.dirname(__file__),
                'data/collection_case1.xml'), 'r') as f:
            response_data = f.read()
        requests_get.return_value.status_code = 200
        requests_get.return_value.content = response_data

        collection = self.client.get_collection()

        self.assertNotIsInstance(collection.next, hatena_blog.Collection)

    @mock.patch('requests.Session.get')
    def test_collection_next(self, requests_get):
        """正常系(次があるケース)"""
        with open(
                os.path.join(os.path.dirname(__file__),
                'data/collection_case_has_next.xml'), 'r') as f:
            response_data = f.read()
        requests_get.return_value.status_code = 200
        requests_get.return_value.content = response_data

        collection = self.client.get_collection()

        self.assertIsInstance(collection.next, hatena_blog.Collection)


class TestEntry(unittest.TestCase):
    def setUp(self):
        self.client = _get_client()
        self.entry = self.client.get_entry()
        self.entry.title='sample title'
        self.entry.content='sample content'
        self.entry.content_type='sample content_type'
        self.entry.is_public=True
        self.entry.categories=['category1', 'category2']
        self.entry.publish_date=datetime.datetime.now()
        self.entry.update_date=datetime.datetime.now()
        self.entry.url='https://hatenablog.com'
        self.entry.entry_id='x3mcln2ix934mf'

    def test_entry_title(self):
        self.assertEqual(self.entry.title, 'sample title')

    def test_entry_content(self):
        self.assertEqual(self.entry.content, 'sample content')

    def test_entry_content_type(self):
        self.assertEqual(self.entry.content_type, 'sample content_type')

    def test_entry_is_public(self):
        self.assertTrue(self.entry.is_public)

    def test_entry_categories(self):
        self.assertEqual(self.entry.categories, ['category1', 'category2'])

    def test_entry_publish_date(self):
        self.assertIsInstance(self.entry.publish_date, datetime.datetime)

    def test_entry_update_date(self):
        self.assertIsInstance(self.entry.update_date, datetime.datetime)

    def test_entry_url(self):
        self.assertEqual(self.entry.url, 'https://hatenablog.com')

    def test_entry_entry_id(self):
        self.assertEqual(self.entry.entry_id, 'x3mcln2ix934mf')

    @mock.patch('requests.post')
    def test_entry_push(self, requests_post):
        self.entry.push()
        requests_post.assert_called_once()
        self.assertTrue(
            'https://blog.hatena.ne.jp/' in requests_post.call_args[0][0]
        )

    @mock.patch('requests.post')
    def test_entry_empty_push(self, requests_post):
        empty_entry = self.client.get_entry()
        with self.assertRaises(hatena_blog.ValidationError):
            empty_entry.push()
        requests_post.assert_not_called()

    @mock.patch('requests.get')
    def test_entry_pull(self, requests_get):
        self.entry.pull()
        requests_get.assert_called_once()
        self.assertTrue(
            'https://blog.hatena.ne.jp/' in requests_get.call_args[0][0]
        )

    @mock.patch('requests.post')
    def test_entry_unpublish(self, requests_post):
        self.entry.is_public = True
        self.assertTrue(self.entry.is_public)
        self.entry.unpublish()
        requests_post.assert_called_once()
        self.assertFalse(self.entry.is_public)
        self.assertTrue(
            'https://blog.hatena.ne.jp/' in requests_post.call_args[0][0]
        )

    @mock.patch('requests.post')
    def test_entry_publish(self, requests_post):
        self.entry.is_public = False
        self.assertFalse(self.entry.is_public)
        self.entry.publish()
        requests_post.assert_called_once()
        self.assertTrue(self.entry.is_public)
        self.assertTrue(
            'https://blog.hatena.ne.jp/' in requests_post.call_args[0][0]
        )
