import requests

HATENA_ATOM_ENDPOINT = "https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom"

class ValidationError(Exception):
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
            url=None,
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
        self.url = url
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
    def __init__(self, category=None):
        self.category = category

    @property
    def entries(self):
        return [Entry()]

    @property
    def public_entries(self):
        return [Entry(is_public=True)]

    @property
    def draft_entries(self):
        return [Entry(is_public=False)]

    @property
    def next(self):
        return Collection()

class Client:
    def __init__(self, hatena_id, blog_id, api_key):
        self.hatena_id = hatena_id
        self.blog_id = blog_id
        self.api_key = api_key

    def get_collection(self, category=None):
        return Collection(category=category)

    def get_entry(self, entry_id=None):
        return Entry(entry_id=entry_id, client=self)

    def push_entry(self, entry):
        requests.post(HATENA_ATOM_ENDPOINT + '/entry')

    def pull_entry(self, entry):
        requests.get(HATENA_ATOM_ENDPOINT + '/entry')
