"""
Provides intermediate representation for markdown text to be converted to `HTMLNode`s
"""
from enum import Enum
from src.htmlnode import LeafNode

TextNodeType = Enum("TextNodeType", ["Text", "Bold", "Italic", "Code", "Link", "Image"])

class TextNode:
    """Class for representing markdown text and converting to `HTMLNodes`"""
    def __init__(
            self,
            text: str,
            text_type: TextNodeType,
            url: str | None = None
        ):
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
            case TextNodeType.Text:
                return LeafNode(None, self.text)
            case TextNodeType.Bold:
                return LeafNode("b", self.text)
            case TextNodeType.Italic:
                return LeafNode("i", self.text)
            case TextNodeType.Code:
                return LeafNode("code", self.text)
            case TextNodeType.Link:
                props = {"href": self.url}
                return LeafNode("a", self.text, props)
            case TextNodeType.Image:
                props = {"src": self.url, "alt": self.text}
                return LeafNode("img", "", props)
            case _:
                raise ValueError(
                    "TextNode.text_type must be one of text, bold, italic, code, link, or image"
                )
