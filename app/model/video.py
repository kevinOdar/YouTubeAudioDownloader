class Video:
    def __init__(self, title, url, thumbnail_url) -> None:
        self.title = title
        self.url = url
        self.thumbnail_url = thumbnail_url

    def __iter__(self):
        yield self.title
        yield self.url
        yield self.thumbnail_url
