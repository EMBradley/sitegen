"""
`sitegen` is a static site generation tool that converts markdown to html.
This package was created as part of the author's completion of Boot.dev's
backend developer course.
"""
from src.textnode import TextNode


def main():
    """Entry point for `sitegen`"""
    node = TextNode("hello world", "bold", "https://www.boot.dev")
    print(node)


main()
