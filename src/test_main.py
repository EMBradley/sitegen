# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

import unittest
from main import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes,
    split_nodes_images,
    split_nodes_links,
)
from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_nodes_code(self):
        node_with_code_block = TextNode(
            "This is text with a `code block` word", TextType.Normal
        )
        new_nodes = split_nodes([node_with_code_block], "`", TextType.Code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.Normal),
                TextNode("code block", TextType.Code),
                TextNode(" word", TextType.Normal),
            ],
        )

    def test_split_nodes_bold(self):
        node_with_bold = TextNode(
            "This node has **bold text** and some **more** bold text", TextType.Normal
        )
        new_nodes = split_nodes([node_with_bold], "**", TextType.Bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This node has ", TextType.Normal),
                TextNode("bold text", TextType.Bold),
                TextNode(" and some ", TextType.Normal),
                TextNode("more", TextType.Bold),
                TextNode(" bold text", TextType.Normal),
            ],
        )

    def test_split_nodes_mixed(self):
        mixed_type = TextNode(
            "This node has a `code block`, some **bold text**, and some *italicized text*",
            TextType.Normal,
        )
        new_nodes = split_nodes([mixed_type], "`", TextType.Code)
        new_nodes = split_nodes(new_nodes, "**", TextType.Bold)
        new_nodes = split_nodes(new_nodes, "*", TextType.Italic)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This node has a ", TextType.Normal),
                TextNode("code block", TextType.Code),
                TextNode(", some ", TextType.Normal),
                TextNode("bold text", TextType.Bold),
                TextNode(", and some ", TextType.Normal),
                TextNode("italicized text", TextType.Italic),
            ],
        )


class TestSplitNodeImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.Normal,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is text with an ", TextType.Normal),
                TextNode(
                    "image",
                    TextType.Image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.Normal),
                TextNode(
                    "second image",
                    TextType.Image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_split_only_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [a link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.Normal,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is text with an ", TextType.Normal),
                TextNode(
                    "image",
                    TextType.Image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(
                    " and [a link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                    TextType.Normal,
                ),
            ],
        )

    def test_no_images_does_nothing(self):
        node = TextNode(
            "This node doesn't have any images but it does have [a link](https://www.boot.dev) and an ![incomplete image]",
            TextType.Normal,
        )
        self.assertEqual(split_nodes_images([node]), [node])


class TestSplitNodeLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is a text node with [a link](https://www.boot.dev) and [another link](https://www.codecademy.com)",
            TextType.Normal,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode(
                    "This is a text node with ",
                    TextType.Normal,
                ),
                TextNode(
                    "a link",
                    TextType.Link,
                    "https://www.boot.dev",
                ),
                TextNode(
                    " and ",
                    TextType.Normal,
                ),
                TextNode(
                    "another link",
                    TextType.Link,
                    "https://www.codecademy.com",
                ),
            ],
        )

    def test_split_only_links(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [a link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.Normal,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode(
                    "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ",
                    TextType.Normal,
                ),
                TextNode(
                    "a link",
                    TextType.Link,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_no_links_does_nothing(self):
        node = TextNode(
            "This node has an ![image](https://example.com) but no link",
            TextType.Normal,
        )
        self.assertEqual(split_nodes_links([node]), [node])


class TestExtractImages(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_extract_no_images(self):
        no_images = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_images(no_images), [])

    def test_no_extract_partial_image(self):
        partial_image = "This text has ![alt text] without an image url and a !(url.com) with no alt text"
        self.assertEqual(extract_markdown_images(partial_image), [])

    def test_extract_only_image_when_link_present(self):
        image_and_link = "This text has ![an image](https://www.test.com) and [a link](https://www.example.com)"
        self.assertEqual(
            extract_markdown_images(image_and_link),
            [("an image", "https://www.test.com")],
        )


class TestExtractLinks(unittest.TestCase):
    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_extract_no_links(self):
        no_link = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_links(no_link), [])

    def test_no_extract_partial_link(self):
        partial_link = "This text has a [link name] and (url.com) but not together"
        self.assertEqual(extract_markdown_links(partial_link), [])

    def test_extract_only_link_when_image_present(self):
        image_and_link = "This text has ![an image](https://www.test.com) and [a link](https://www.example.com)"
        self.assertEqual(
            extract_markdown_links(image_and_link),
            [("a link", "https://www.example.com")],
        )


if __name__ == "__main__":
    unittest.main()
