# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
from textnode import (
        TextNode,
        TextType,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a bold node", TextType.Bold)
        node2 = TextNode("This is a bold node", TextType.Bold)
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("This node has a url", TextType.Bold, "https://www.boot.dev")
        node2 = TextNode("This node has a url", TextType.Bold, "https://www.boot.dev")
        self.assertEqual(node1, node2)

    def test_ne_text(self):
        node1 = TextNode("This is a text node", TextType.Normal)
        node2 = TextNode("This is a different text node", TextType.Normal)
        self.assertNotEqual(node1, node2)

    def test_ne_type(self):
        node1 = TextNode("These nodes have different styles", TextType.Normal)
        node2 = TextNode("These nodes have different styles", TextType.Bold)
        self.assertNotEqual(node1, node2)

    def test_ne_url(self):
        node1 = TextNode("These have different urls", TextType.Bold, "https://www.boot.dev")
        node2 = TextNode(
            "These have different urls",
            TextType.Bold,
            "https://www.codecademy.com"
        )
        self.assertNotEqual(node1, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.Bold)
        self.assertIsNone(node.url)

    def test_with_url(self):
        node = TextNode("This text node has a link", TextType.Bold, "https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")

    def test_repr(self):
        node = TextNode("This text node has a link", TextType.Bold, "https://www.boot.dev")
        self.assertEqual(
            repr(node),
            "TextNode(This text node has a link, TextNodeType.Bold, https://www.boot.dev)"
        )

    def test_to_html(self):
        text_node = TextNode("This is a text node", TextType.Normal)
        bold_node = TextNode("This is a bold node", TextType.Bold)
        italic_node = TextNode("This is an italic node", TextType.Italic)
        code_node = TextNode("print('Hello world')", TextType.Code)
        link_node = TextNode("Boot.dev", TextType.Link, "https://www.boot.dev")
        img_node = TextNode("Autism creature", TextType.Image, "https://bit.ly/4bx5bzq")
        invalid_node = TextNode("This node shouldn't exist", "not a real text_type") # type: ignore

        text_html = text_node.to_html_node().to_html()
        bold_html = bold_node.to_html_node().to_html()
        italic_html = italic_node.to_html_node().to_html()
        code_html = code_node.to_html_node().to_html()
        link_html = link_node.to_html_node().to_html()
        img_html = img_node.to_html_node().to_html()

        self.assertRaises(ValueError, invalid_node.to_html_node)
        self.assertEqual(
            text_html,
            "This is a text node"
        )
        self.assertEqual(
            bold_html,
            "<b>This is a bold node</b>"
        )
        self.assertEqual(
            italic_html,
            "<i>This is an italic node</i>"
        )
        self.assertEqual(
            code_html,
            "<code>print('Hello world')</code>"
        )
        self.assertEqual(
            link_html,
            '<a href="https://www.boot.dev">Boot.dev</a>',
        )
        self.assertEqual(
            img_html,
            '<img src="https://bit.ly/4bx5bzq" alt="Autism creature"></img>',
        )


class TestSplitNode(unittest.TestCase):
    def test_split_nodes_code(self):
        node_with_code_block = TextNode("This is text with a `code block` word", TextType.Normal)
        new_nodes = split_nodes([node_with_code_block], "`", TextType.Code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.Normal),
                TextNode("code block", TextType.Code),
                TextNode(" word", TextType.Normal),
            ]
        )

    def test_split_nodes_bold(self):
        node_with_bold = TextNode(
            "This node has **bold text** and some **more** bold text",
            TextType.Normal
        )
        new_nodes = split_nodes([node_with_bold], "**", TextType.Bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This node has ", TextType.Normal),
                TextNode("bold text", TextType.Bold),
                TextNode(" and some ", TextType.Normal),
                TextNode("more", TextType.Bold),
                TextNode(" bold text", TextType.Normal)
            ]
        )

    def test_split_nodes_mixed(self):
        mixed_type = TextNode(
            "This node has a `code block`, some **bold text**, and some *italicized text*",
            TextType.Normal
        )
        new_nodes = split_nodes([mixed_type], '`', TextType.Code)
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
                TextNode("italicized text", TextType.Italic)
            ]
        )


class TestExtract(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)" # pylint: disable=line-too-long
        self.assertEqual(
            extract_markdown_images(text),
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png" # pylint: disable=line-too-long
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png" # pylint: disable=line-too-long
                )
            ]
        )

    def test_extract_no_images(self):
        no_images = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)" # pylint: disable=line-too-long
        self.assertEqual(
            extract_markdown_images(no_images),
            []
        )

    def test_no_extract_partial_image(self):
        partial_image = "This text has ![alt text] without an image url and a !(url.com) with no alt text" # pylint: disable=line-too-long
        self.assertEqual(
            extract_markdown_images(partial_image),
            []
        )

    def test_extract_only_image_when_link_present(self):
        image_and_link = "This text has ![an image](https://www.test.com) and [a link](https://www.example.com)" # pylint: disable=line-too-long
        self.assertEqual(
            extract_markdown_images(image_and_link),
            [("an image", "https://www.test.com")]
        )

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)" # pylint: disable=line-too-long
        self.assertEqual(
            extract_markdown_links(text),
            [
                (
                    "link",
                    "https://www.example.com"
                ),
                (
                    "another",
                    "https://www.example.com/another"
                )
            ]
        )

    def test_extract_no_links(self):
        no_link = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)" # pylint: disable=line-too-long
        self.assertEqual(
            extract_markdown_links(no_link),
            []
        )

    def test_no_extract_partial_link(self):
        partial_link = "This text has a [link name] and (url.com) but not together"
        self.assertEqual(
            extract_markdown_links(partial_link),
            []
        )

    def test_extract_only_link_when_image_present(self):
        image_and_link = "This text has ![an image](https://www.test.com) and [a link](https://www.example.com)" # pylint: disable=line-too-long
        self.assertEqual(
            extract_markdown_links(image_and_link),
            [("a link", "https://www.example.com")]
        )


if __name__ == "__main__":
    unittest.main()
