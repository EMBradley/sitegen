"""
Provides intermediate representation for html documents as an abstract syntax tree
and allows converting to proper html
"""


class HTMLNode:
    """Abstract parent class for intermediate representation of html nodes"""

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict | None = None,
        children: list | None = None,
    ):
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children

    def __repr__(self):
        return f"HTMLNode(tag={repr(self.tag)}, \
value={repr(self.value)}, children={repr(self.children)}, props={repr(self.props)})"

    def to_html(self):
        """Placeholder method to be overridden by child classes"""
        raise NotImplementedError

    def props_to_html(self) -> str | None:
        """Converts `self.props` to a string for use html tag output"""
        if not self.props:
            return None

        html_props = ""

        for key, value in self.props.items():
            html_props += f' {key}="{value}"'

        return html_props


class LeafNode(HTMLNode):
    """
    Class for html node that has no children.
    Note: `LeafNode`s must have a `value` attribute that is not `None`
    """

    def __init__(self, tag: str | None, value: str, props: dict | None = None):
        super().__init__(tag, value, props)

    def to_html(self) -> str:
        if (self.value != "") and not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value

        if self.props:
            html_props = self.props_to_html()
        else:
            html_props = ""

        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """
    Class for html nodes that have children.
    Note: `ParentNode`s must have a `tag` that is not `None`,
        and a `children` list that is not `None` or empty
    """

    def __init__(self, tag: str, children: list, props: dict | None = None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        if self.props:
            html_props = self.props_to_html()
        else:
            html_props = ""

        opening_tag = f"<{self.tag}{html_props}>"
        closing_tag = f"</{self.tag}>"

        children = ""
        for child in self.children:
            children += child.to_html()

        return f"{opening_tag}{children}{closing_tag}"
