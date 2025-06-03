from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from inline_markdown import *
from block_markdown import *

def main():
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    breakpoint()
    blocks = markdown_to_blocks(md)
    for b in blocks:
        print(b)
if __name__ == "__main__":
    main()
