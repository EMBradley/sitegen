class HTMLNode:
    def __init__(self, tag=None, value=None, props=None, children=None):
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
    def __init__(self, tag=None, value=None, props=None):
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
