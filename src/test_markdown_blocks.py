# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

import unittest

from markdown_blocks import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is a **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is a **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_ignore_empty_blocks(self):
        markdown = """After this block there are extra lines\n\n\n\t\n\t\n\t\t\n
Some of those lines have extra whitespace"""
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "After this block there are extra lines",
                "Some of those lines have extra whitespace",
            ],
        )


if __name__ == "__main__":
    unittest.main()
