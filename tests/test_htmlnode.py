import unittest
from src.htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag='h1', value='this is a heading')
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

    def test_props_to_html(self):
        node = HTMLNode(tag='a', props={'href': 'https://www.boot.dev', 'target': '_blank'})
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.boot.dev" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode()
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag(self):
        node = LeafNode(None, "this node has no tag")
        self.assertEqual(node.to_html(), "this node has no tag")

    def test_with_tag(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')


if __name__ == "__main__":
    unittest.main()
