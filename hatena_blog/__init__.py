import datetime

from dateutil import parser
import requests
from bs4 import BeautifulSoup

HATENA_ATOM_ENDPOINT = "https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom"

class ValidationError(Exception):
    pass

class InvalidRequestsError(Exception):
    pass

class Entry:
    def __init__(self,
            title=None,
            content=None,
            content_type=None,
            is_public=False,
            entry_id=None,
            categories=[],
            publish_date=None,
            update_date=None,
            public_url=None,
            edit_url=None,
            client=None
        ):
        self.title = title
        self.content = content
        self.content_type = content_type
        self.categories = categories
        self.is_public = is_public
        self.entry_id = entry_id
        self.publish_date = publish_date
        self.update_date = update_date
        self.public_url = public_url
        self.edit_url = edit_url
        self.client = client

    def push(self):
        if not self.entry_id or not self.title:
            raise ValidationError("Can't push. because entry doesn't have entry_id.")
        self.client.push_entry(self)

    def pull(self):
        self.client.pull_entry(self)

    def publish(self):
        self.is_public = True
        self.push()

    def unpublish(self):
        self.is_public = False
        self.push()

class Collection:
    def __init__(self, xml, category=None, client=None):
        self._xml = xml
        self.category = category
        self.client = client
        self.entries = []
        self._parse_xml()

    def _parse_xml(self):
        if not self._xml:
            return

        soup = BeautifulSoup(self._xml, 'html.parser')
        soup_entries = soup.find_all('entry')
        for soup_entry in soup_entries:
            entry = Entry(
                client=self.client,
                title=soup_entry.title.string,
                content=soup_entry.content.string,
                content_type=soup_entry.content['type'],
                update_date=parser.parse(soup_entry.updated.string),
                publish_date=parser.parse(soup_entry.published.string),
                public_url=soup_entry.find('link', rel='alternate')['href'],
                edit_url=soup_entry.find('link', rel='edit')['href'],
                entry_id=soup_entry.id.string.split('-')[-1],
            )

            draft = soup_entry.find('app:draft').string
            if draft == 'no':
                entry.is_public=True

            soup_categories = soup_entry.find_all('category')
            for soup_category in soup_categories:
                category = soup_category['term']
                entry.categories.append(category)

            self.entries.append(entry)

    @property
    def public_entries(self):
        return [Entry(is_public=True)]

    @property
    def draft_entries(self):
        return [Entry(is_public=False)]

    @property
    def next(self):
        return self.client.get_collection()

class Client:
    def __init__(self, hatena_id, blog_id, api_key):
        self.hatena_id = hatena_id
        self.blog_id = blog_id
        self.api_key = api_key
        self.session = requests.session()
        self.endpoint = HATENA_ATOM_ENDPOINT.format(hatena_id=self.hatena_id, blog_id=self.blog_id)

    def get_collection(self, category=None):
        response = self.session.get(self.endpoint+'/entry', auth=(self.hatena_id, self.api_key))
        if response.status_code != 200:
            raise InvalidRequestsError
        return Collection(xml=response.content, category=category, client=self)

    def get_entry(self, entry_id=None):
        return Entry(entry_id=entry_id, client=self)

    def push_entry(self, entry):
        requests.post(HATENA_ATOM_ENDPOINT + '/entry')

    def pull_entry(self, entry):
        requests.get(HATENA_ATOM_ENDPOINT + '/entry')
