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
    def test_get_entries_top_3(self):

        client = hatena_blog.Client(
                        hatena_id=HATENA_ID,
                        blog_id=HATENA_BLOG_ID,
                        api_key=HATENA_API_KEY)
        recorder = betamax.Betamax(
            client.session, cassette_library_dir=CASSETTE_LIBRARY_DIR
        )

        with recorder.use_cassette('test_get_entries_top_3', serialize_with='prettyjson'):
            collection = client.get_collection()
            entries = collection.entries
            self.assertEqual(entries[0].title, 'テスト用の記事7')
            self.assertEqual(entries[1].title, 'テスト用の記事6')
            self.assertEqual(entries[2].title, 'テスト用の記事5')

