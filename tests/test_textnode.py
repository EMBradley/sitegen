import unittest
from src.textnode import TextNode
from src.htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a bold node", "bold")
        node2 = TextNode("This is a bold node", "bold")
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("This node has a url", "bold", "https://www.boot.dev")
        node2 = TextNode("This node has a url", "bold", "https://www.boot.dev")
        self.assertEqual(node1, node2)

    def test_ne_text(self):
        node1 = TextNode("This is a text node", "text")
        node2 = TextNode("This is a different text node", "text")
        self.assertNotEqual(node1, node2)

    def test_ne_type(self):
        node1 = TextNode("These nodes have different styles", "text")
        node2 = TextNode("These nodes have different styles", "bold")
        self.assertNotEqual(node1, node2)

    def test_ne_url(self):
        node1 = TextNode("These have different urls", "bold", "https://www.boot.dev")
        node2 = TextNode("These have different urls", "bold", "https://www.codecademy.com")
        self.assertNotEqual(node1, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)

    def test_with_url(self):
        node = TextNode("This text node has a link", "bold", "https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")

    def test_repr(self):
        node = TextNode("This text node has a link", "bold", "https://www.boot.dev")
        self.assertEqual(
            repr(node),
            "TextNode(This text node has a link, bold, https://www.boot.dev)"
        )

    def test_to_html(self):
        text_node = TextNode("This is a text node", "text")
        bold_node = TextNode("This is a bold node", "bold")
        italic_node = TextNode("This is an italic node", "italic")
        code_node = TextNode("print('Hello world')", "code")
        link_node = TextNode("Boot.dev", "link", "https://www.boot.dev")
        img_node = TextNode(
            "Autism creature",
            "image",
            "https://img.freepik.com/premium-vector/autism-tbh-creature-meme-kids-meme-autistic-among-us-mascot-autism-awareness-funny_687076-75.jpg?w=740"
        )
        invalid_node = TextNode("This node shouldn't exist", "not a real text_type")

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
            '<img \
src="https://img.freepik.com/premium-vector/autism-tbh-creature-meme-kids-meme-autistic-among-us-mascot-autism-awareness-funny_687076-75.jpg?w=740" \
alt="Autism creature"></img>',
        )



if __name__ == "__main__":
    unittest.main()
