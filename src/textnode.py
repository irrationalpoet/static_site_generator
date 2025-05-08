from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    TXT_LINK = "txt_link"
    IMG_LINK = "img_link"

class TextNode:
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    
