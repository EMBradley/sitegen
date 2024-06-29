# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        node = LeafNode(None, None) # type: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag(self):
        node = LeafNode(None, "this node has no tag") # type: ignore
        self.assertEqual(node.to_html(), "this node has no tag")

    def test_with_tag(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        node = ParentNode(None, [LeafNode(None, "some text")]) # type: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_no_children(self):
        node_none_children = ParentNode("p", None) # type: ignore
        node_empty_children = ParentNode("p", [])

        self.assertRaises(ValueError, node_none_children.to_html)
        self.assertRaises(ValueError, node_empty_children.to_html)

    def test_nested_broken_inside(self):
        node_none_children_inside = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode("ul", None), # type: ignore
                LeafNode("i", "italic text"),
            ]
        )
        node_empty_children_inside = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("ol", []),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ]
        )
        node_no_tag_inside = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(None, [LeafNode(None, "some text")]), # type: ignore
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ]
        )


        self.assertRaises(ValueError, node_none_children_inside.to_html)
        self.assertRaises(ValueError, node_empty_children_inside.to_html)
        self.assertRaises(ValueError, node_no_tag_inside.to_html)


    def test_single_layer(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        )

    def test_nested(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "a numbered list item"),
                        LeafNode("li", "a second list item"),
                    ]
                ),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "a bullet point"),
                        LeafNode("li", "another bullet point"),
                    ]
                ),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b><ol><li>a numbered list item</li>\
<li>a second list item</li></ol>Normal text<i>italic text</i><ul>\
<li>a bullet point</li><li>another bullet point</li></ul>Normal text</p>"
        )

    def test_three_levels(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "a numbered list item"),
                        LeafNode("li", "a second list item"),
                        ParentNode("li", [LeafNode("i", "an italicized list item")])
                    ]
                ),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "a bullet point"),
                        LeafNode("li", "another bullet point"),
                    ]
                ),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b><ol><li>a numbered list item</li><li>a second list item</li>\
<li><i>an italicized list item</i></li></ol>Normal text<i>italic text</i><ul>\
<li>a bullet point</li><li>another bullet point</li></ul>Normal text</p>"
        )


if __name__ == "__main__":
    unittest.main()
