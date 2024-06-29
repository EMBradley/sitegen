class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

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
