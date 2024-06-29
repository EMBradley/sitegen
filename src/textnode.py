class TextNode:
    def __init__(
            self,
            text: str,
            text_type: str,
            url: str | None = None
        ):
        assert (isinstance(text, str))
        assert (isinstance(text_type, str))
        assert (url is None or isinstance(url, str))

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
