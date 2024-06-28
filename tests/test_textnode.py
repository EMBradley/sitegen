import unittest

from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("These nodes have urls", "bold", "https://www.boot.dev")
        node2 = TextNode("These nodes have urls", "bold", "https://www.boot.dev")
        self.assertEqual(node1, node2)

    def test_ne_text(self):
        node1 = TextNode("This is a text node", "normal")
        node2 = TextNode("This is a different text node", "normal")
        self.assertNotEqual(node1, node2)

    def test_ne_type(self):
        node1 = TextNode("These nodes have different styles", "normal")
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


if __name__ == "__main__":
    unittest.main()
