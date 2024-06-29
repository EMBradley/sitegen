"""
`sitegen` is a static site generation tool that converts markdown to html.
This package was created as part of the author's completion of Boot.dev's
backend developer course.
"""

import re
from typing import List, Tuple
from textnode import TextNode, TextType


def main():
    """Entry point for `sitegen`"""
    node = TextNode("hello world", TextType.Bold, "https://www.boot.dev")
    print(node)


def split_nodes(
    nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
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

        for i, chunk in enumerate(chunks):
            if not chunk:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(chunk, TextType.Normal))
            else:
                new_nodes.append(TextNode(chunk, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Finds all markdown images in given text. Images are represented in markdown by strings
    of the form ![alt text](link to image). This function returns all images in the given text
    in the form of a list of (alt text, link) tuples.
    """
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Finds all markdown links in given text. Images are represented in markdown by strings
    of the form [link text](url). This function returns all images in the given text
    in the form of a list of (link text, url) tuples.
    """
    return re.findall(r"(?:[^!])\[(.*?)\]\((.*?)\)", text)


if __name__ == "__main__":
    main()
