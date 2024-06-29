import unittest
from src.htmlnode import HTMLNode

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



if __name__ == "__main__":
    unittest.main()
