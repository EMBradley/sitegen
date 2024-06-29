"""
`sitegen` is a static site generation tool that converts markdown to html.
This package was created as part of the author's completion of Boot.dev's
backend developer course.
"""
from .textnode import TextNode, TextType


def main():
    """Entry point for `sitegen`"""
    node = TextNode("hello world", TextType.Bold, "https://www.boot.dev")
    print(node)


main()
