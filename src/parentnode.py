from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("must have tag")
        if not self.children:
            raise ValueError("must have children")
        return f'<{self.tag}>{"".join([child.to_html() for child in self.children])}</{self.tag}>'
        #return f'<{self.tag}>{"".join(map(lambda child: child.to_html(), self.children))}</{self.tag}>'
