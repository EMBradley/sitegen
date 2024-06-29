class HTMLNode:
    def __init__(
            self,
            tag: str | None = None,
            value: str | None = None,
            props: dict | None = None,
            children: list | None = None
        ):
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children

    def __repr__(self):
        return f"HTMLNode(tag={repr(self.tag)}, value={repr(self.value)}, children={repr(self.children)}, props={repr(self.props)})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return

        html_props = ""

        for (key, value) in self.props.items():
            html_props += f' {key}="{value}"'

        return html_props

class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str | None,
            value: str,
            props: dict | None = None
        ):
        super().__init__(tag, value, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value

        html_props = ""
        if self.props:
            html_props = self.props_to_html()

        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: list,
            props: dict | None = None
        ):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        html_props = ""
        if self.props:
            html_props = self.props_to_html()

        opening_tag = f"<{self.tag}{html_props}>"
        closing_tag = f"</{self.tag}>"
        
        children = ""
        for child in self.children:
            children += child.to_html()

        return f"{opening_tag}{children}{closing_tag}"
