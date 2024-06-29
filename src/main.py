"""
`sitegen` is a static site generation tool that converts markdown to html.
This package was created as part of the author's completion of Boot.dev's
backend developer course.
"""

import re
from textnode import TextNode, TextType


def main():
    """Entry point for `sitegen`"""
    node = TextNode("hello world", TextType.Bold, "https://www.boot.dev")
    print(node)


def split_nodes(
    nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Splits a list of `TextNode`s into a new list where text between a pair of `delimiters`
    has been separated into a new node of type `text_type`
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


def split_nodes_images(nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits a list of `TextNode`s into a new list where all markdown images embedded in
    `TextNode`s with the `Normal` type have been extracted to separate nodes.
    """
    new_nodes = []

    for node in nodes:
        if node.text_type != TextType.Normal:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        text = node.text

        for image in images:
            chunks = text.split(f"![{image[0]}]({image[1]})", 1)

            if chunks[0]:
                normal_node = TextNode(chunks[0], TextType.Normal)
                new_nodes.append(normal_node)

            image_node = TextNode(image[0], TextType.Image, image[1])
            new_nodes.append(image_node)

            text = chunks[1]

        if text:
            new_nodes.append(TextNode(text, TextType.Normal))

    return new_nodes


def split_nodes_links(nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits a list of `TextNode`s into a new list where all markdown links embedded in
    `TextNode`s with the `Normal` type have been extracted to separate nodes.
    """
    new_nodes = []

    for node in nodes:
        if node.text_type != TextType.Normal:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        text = node.text

        for link in links:
            chunks = text.split(f"[{link[0]}]({link[1]})", 1)

            if chunks[0]:
                normal_node = TextNode(chunks[0], TextType.Normal)
                new_nodes.append(normal_node)

            image_node = TextNode(link[0], TextType.Link, link[1])
            new_nodes.append(image_node)

            text = chunks[1]

        if text:
            new_nodes.append(TextNode(text, TextType.Normal))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Finds all markdown images in given text. Images are represented in markdown by strings
    of the form ![alt text](link to image). This function returns all images in the given text
    in the form of a list of (alt text, link) tuples.
    """
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Finds all markdown links in given text. Images are represented in markdown by strings
    of the form [link text](url). This function returns all images in the given text
    in the form of a list of (link text, url) tuples.
    """
    return re.findall(r"(?:[^!])\[(.*?)\]\((.*?)\)", text)


if __name__ == "__main__":
    main()
