"""
Provides intermediate representation for markdown text to be converted to `HTMLNode`s
"""
from typing import List
from enum import Enum
from src.htmlnode import LeafNode

TextType = Enum("TextNodeType", ["Normal", "Bold", "Italic", "Code", "Link", "Image"])

class TextNode:
    """Class for representing markdown text and converting to `HTMLNodes`"""
    def __init__(
            self,
            text: str,
            text_type: TextType,
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
            case TextType.Normal:
                return LeafNode(None, self.text)
            case TextType.Bold:
                return LeafNode("b", self.text)
            case TextType.Italic:
                return LeafNode("i", self.text)
            case TextType.Code:
                return LeafNode("code", self.text)
            case TextType.Link:
                props = {"href": self.url}
                return LeafNode("a", self.text, props)
            case TextType.Image:
                props = {"src": self.url, "alt": self.text}
                return LeafNode("img", "", props)
            case _:
                raise ValueError(
                    "TextNode.text_type must be one of text, bold, italic, code, link, or image"
                )

def split_nodes(nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """
    Splits each of the `Text` nodes in `nodes`, and inserts nodes of type `text_type`
    between each pair of `delimiters`
    """
    new_nodes = []

    for node in nodes:
        if node.text_type != TextType.Normal:
            new_nodes.append(node)
            continue
        if not delimiter in node.text:
            new_nodes.append(node)
            continue

        chunks = node.text.split(delimiter)

        # an even number of delimiters splits the text into an odd number of chunks,
        # so if there are an even number of chunks then there are mismatched delimiters
        if len(chunks) % 2 == 0:
            raise ValueError("Unclosed delimiter found")

        for (i, chunk) in enumerate(chunks):
            if not chunk:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(chunk, TextType.Normal))
            else:
                new_nodes.append(TextNode(chunk, text_type))


    return new_nodes
