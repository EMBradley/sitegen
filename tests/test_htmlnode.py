import unittest
from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="h1", value="this is a heading")
        self.assertEqual(
            repr(node),
            "HTMLNode(tag='h1', value='this is a heading', children=None, props=None)"
        )

    def test_default(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)



if __name__ == "__main__":
    unittest.main()
