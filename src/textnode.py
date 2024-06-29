"""
Provides intermediate representation for markdown text to be converted to `HTMLNode`s
"""
from src.htmlnode import LeafNode


class TextNode:
    """Class for representing markdown text and converting to `HTMLNodes`"""
    def __init__(
            self,
            text: str,
            text_type: str,
            url: str | None = None
        ):
        assert isinstance(text, str)
        assert isinstance(text_type, str)
        assert url is None or isinstance(url, str)

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

    def to_html_node(self) -> LeafNode:
        """Converts `self` into an html `LeafNode`"""
        match self.text_type:
            case "text":
                return LeafNode(None, self.text)
            case "bold" | "italic":
                return LeafNode(self.text_type[0], self.text)
            case "code":
                return LeafNode("code", self.text)
            case "link":
                props = {"href": self.url}
                return LeafNode("a", self.text, props)
            case "image":
                props = {"src": self.url, "alt": self.text}
                return LeafNode("img", "", props)
            case _:
                raise ValueError(
                    "TextNode.text_type must be one of text, bold, italic, code, link, or image"
                )
