# hatena_blog

Hatena Blog のAPI Wrapperです。.

# インストール方法

次のようにインストールできます。

```
$ pip install git+https://github.com/mtb-beta/hatena_blog
```

# 使い方

次のようにimportできます。

```
import hatena_blog
```

クライアントオブジェクトを次のように初期化します。

```
hatena_id = "your_hatena_id"
blog_id = "your_blog_id"
api_key = "your_api_key"
client = hatena_blog.Client(
    hatena_id=hatena_id,
    blog_id=blog_id,
    api_key=api_key
)
```

次のようにすると、Entry（記事）のCollection（一覧）が取得できます。
```
collection = client.get_collection()
```

次のようにすると、Collectionに含まれるEntryのリストが取れます。
```
collection.entries
```

これで次のページのコレクションがとれます。
```
collection.next
```

これで公開状態のエントリーリストが取れます。

```
collection.public_entries
```


これで下書きのエントリーリストが取れます。
```
collection.draft_entries
```

これで指定したエントリーが取れます。
```
entry = client.get_entry(entry_id)
```

こんな感じで、プロパティにアクセスできる。
```
entry.entry_id
entry.title
entry.content
entry.content_type
entry.is_public
entry.categories
entry.publish_date
entry.update_date
entry.url
```

これで、はてなブログに情報を送れます。
```
entry.push()
```

これで、はてなブログから情報を再取得します。
```
entry.pull()
```

これで、はてなブログに送りつつ公開します。
```
entry.publish()
```

これで、はてなブログに送りつつ下書きにします。
```
entry.unpublish()
```

こんな風に空を指定すると空の記事を作れる。
```
entry= client.get_entry()
```

何も書いてない記事はpush()できない。要は保存できない。
```
entry.push() # error!
```


# Test

If you want to test, execute next commands.

```
$ tox
```
