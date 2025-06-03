from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            err = f"invalid markdown syntax, {delimiter} not closed"
            raise ValueError(err)
        sections = old_node.text.split(delimiter)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        old_node_txt = old_node.text
        if old_node_txt == "":
            continue
        md_links = extract_markdown_images(old_node_txt)
        if len(md_links) == 0:
            new_nodes.append(old_node)
            continue
        for alt_txt, img_link in md_links:
            new_node_txt, old_node_txt = old_node_txt.split(f"![{alt_txt}]({img_link})", 1)
            if new_node_txt != "":
                new_nodes.append(TextNode(new_node_txt, TextType.TEXT))
            new_nodes.append(TextNode(alt_txt, TextType.IMAGE, img_link))
        if old_node_txt != "":
            new_nodes.append(TextNode(old_node_txt, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        old_node_txt = old_node.text
        if old_node_txt == "":
            continue
        md_links = extract_markdown_links(old_node_txt)
        if len(md_links) == 0:
            new_nodes.append(old_node)
            continue
        for alt_txt, link in md_links:
            new_node_txt, old_node_txt = old_node_txt.split(f"[{alt_txt}]({link})", 1)
            if new_node_txt != "":
                new_nodes.append(TextNode(new_node_txt, TextType.TEXT))
            new_nodes.append(TextNode(alt_txt, TextType.LINK, link))
        if old_node_txt != "":
            new_nodes.append(TextNode(old_node_txt, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            new_nodes.extend(split_nodes_image([old_node]))
        else:
            new_nodes.append(old_node)

    old_nodes = new_nodes
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            new_nodes.extend(split_nodes_link([old_node]))
        else:
            new_nodes.append(old_node)

    for delimiter, text_type in [ ("**", TextType.BOLD), ("_", TextType.ITALIC), ("'", TextType.CODE) ]:
        old_nodes = new_nodes
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type == TextType.TEXT:
               new_nodes.extend(split_nodes_delimiter([old_node], delimiter, text_type))
            else:
                new_nodes.append(old_node)

    return new_nodes
