# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

import unittest

from htmlnode import LeafNode, ParentNode
from markdown_blocks import (
    BlockType,
    get_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is a **bolded** paragraph

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

    def test_block_type(self):
        blocks = [
            (
                BlockType.Heading,
                [
                    "# Heading 1",
                    "## Heading 2",
                    "### Heading 3",
                    "#### Heading 4",
                    "##### Heading 5",
                    "###### Heading 6",
                ],
            ),
            (
                BlockType.Code,
                [
                    "```this is a code block```",
                    "```\nthis is a multiline code block\n```",
                ],
            ),
            (
                BlockType.Quote,
                [
                    "> It is a truth universally acknowledged",
                    "> Roses are red\n> Violets are blue\n> Markdown is easy\n> HTML is too",
                ],
            ),
            (
                BlockType.UnorderedList,
                [
                    "* this is\n* an unordered\n* list",
                    "- this list\n- has different\n- bullet points",
                    "- this list\n* uses mixed\n* bullet point\n- styles",
                ],
            ),
            (
                BlockType.OrderedList,
                [
                    "1. This list\n2. Has numbered items\n3. Instead of bullet points",
                    "1. This ordered list has only one item",
                ],
            ),
            (
                BlockType.Paragraph,
                [
                    "",  # there shouldn't be empty blocks, but if there are they should be paragraphs
                    "This is a normal paragraph",
                    "####### This has too many #'s to be a heading",
                    "> This block\n* mixes quotes and unordered lists\n- so it is neither",
                    ">This quote block\n>is missing spaces after lead characters",
                    "1. This ordered list\n3. is out of order",
                    "2. This ordered list\n3. doesn't start at 1",
                    "1. This ordered list\n* has an\n- unordered list\n2. in the middle",
                ],
            ),
        ]

        for block_type, blocks in blocks:
            for block in blocks:
                self.assertEqual(get_block_type(block.strip()), block_type)

    def test_markdown_to_html_node(self):
        markdown = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

```
print("Hello world")
```

> We are the hollow men
> We are the stuffed men
> Leaning together
> Headpiece filled with straw. Alas!

* bullet
* points

* more
- bullet
- points

1. a
2. list
3. in
4. order

a paragraph of normal text
        """

        html_node = ParentNode(
            "div",
            [
                ParentNode("h1", [LeafNode(None, "Heading 1")]),
                ParentNode("h2", [LeafNode(None, "Heading 2")]),
                ParentNode("h3", [LeafNode(None, "Heading 3")]),
                ParentNode("h4", [LeafNode(None, "Heading 4")]),
                ParentNode("h5", [LeafNode(None, "Heading 5")]),
                ParentNode("h6", [LeafNode(None, "Heading 6")]),
                ParentNode(
                    "pre",
                    [ParentNode("code", [LeafNode(None, 'print("Hello world")')])],
                ),
                ParentNode(
                    "blockquote",
                    [
                        LeafNode(
                            None,
                            "We are the hollow men\nWe are the stuffed men\nLeaning together\nHeadpiece filled with straw. Alas!",
                        )
                    ],
                ),
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "bullet")]),
                        ParentNode("li", [LeafNode(None, "points")]),
                    ],
                ),
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "more")]),
                        ParentNode("li", [LeafNode(None, "bullet")]),
                        ParentNode("li", [LeafNode(None, "points")]),
                    ],
                ),
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode(None, "a")]),
                        ParentNode("li", [LeafNode(None, "list")]),
                        ParentNode("li", [LeafNode(None, "in")]),
                        ParentNode("li", [LeafNode(None, "order")]),
                    ],
                ),
                ParentNode("p", [LeafNode(None, "a paragraph of normal text")]),
            ],
        )

        self.assertEqual(markdown_to_html_node(markdown).to_html(), html_node.to_html())


if __name__ == "__main__":
    unittest.main()
