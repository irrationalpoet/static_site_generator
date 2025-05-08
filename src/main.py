from textnode import TextNode
from textnode import TextType

def main():
    txt_node = TextNode("hello world", TextType.BOLD, "https://irrationalpoet.com")
    print(txt_node)

if __name__ == "__main__":
    main()
