import unittest
import os
import betamax
from betamax_serializers import pretty_json
import hatena_blog
from dotenv import load_dotenv

load_dotenv('.env')

HATENA_ID = os.environ.get('HATENA_ID')
HATENA_BLOG_ID = os.environ.get('HATENA_BLOG_ID')
HATENA_API_KEY = os.environ.get('HATENA_API_KEY')
CASSETTE_LIBRARY_DIR = "cassettes/"

betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)

class TestSenarioCollectEntry(unittest.TestCase):
    def setUp(self):
        self.client = hatena_blog.Client(
                        hatena_id=HATENA_ID,
                        blog_id=HATENA_BLOG_ID,
                        api_key=HATENA_API_KEY)
        self.recorder = betamax.Betamax(
            self.client.session, cassette_library_dir=CASSETTE_LIBRARY_DIR
        )

    def test_get_entries(self):
        with self.recorder.use_cassette('test_get_entries', serialize_with='prettyjson'):
            collection = self.client.get_collection()
            entries = collection.entries
            for entry in entries:
                self.assertIsInstance(entry, hatena_blog.Entry)

    def test_get_draft_entries(self):
        with self.recorder.use_cassette('test_get_entries', serialize_with='prettyjson'):
            collection = self.client.get_collection()
            entries = collection.draft_entries
            for entry in entries:
                self.assertFalse(entry.is_public)

    def test_get_public_entries(self):
        with self.recorder.use_cassette('test_get_entries', serialize_with='prettyjson'):
            collection = self.client.get_collection()
            entries = collection.public_entries
            for entry in entries:
                self.assertTrue(entry.is_public)

    def test_get_next(self):
        with self.recorder.use_cassette('test_get_next', serialize_with='prettyjson'):
            collection = self.client.get_collection()
            entries = collection.entries
            self.assertTrue(len(entries) > 0)
            next_entries = collection.next.entries
            for entry in next_entries:
                self.assertIsInstance(entry, hatena_blog.Entry)

            self.assertNotEqual(entries, next_entries)


