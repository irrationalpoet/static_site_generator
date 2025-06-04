import unittest
from textnode import *
from inline_markdown import *
from block_markdown import *

class TestNode(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is a text with a 'code block' word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)

    def test_multiple_nodes(self):
        nodes = [
                TextNode("This is a text with a 'code block' word", TextType.TEXT),
                TextNode("This is a text with an _italic_ word", TextType.TEXT),
                TextNode("This is a text with a *bold* word", TextType.TEXT)
                ]
        new_nodes = []
        for node in nodes:
            if "'" in node.text:
                new_nodes.extend(split_nodes_delimiter([node], "'", TextType.CODE))
            elif "_" in node.text:
                new_nodes.extend(split_nodes_delimiter([node], "_", TextType.ITALIC))
            elif "*" in node.text:
                new_nodes.extend(split_nodes_delimiter([node], "*", TextType.BOLD))
            else:
                new_nodes.append(node)

    def test_improper_markdown_syntax(self):
        node = TextNode("This is improperly formatted *markdown syntax", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_not_normal_text(self):
        node = TextNode("'This is not normal text'", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded", TextType.BOLD),
                    TextNode(" word", TextType.TEXT),
                    ],
                new_nodes,
                )

    def test_delim_bold_double(self):
        node = TextNode(
                "This is text with a **bolded** word and **another**", TextType.TEXT
                )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded", TextType.BOLD),
                    TextNode(" word and ", TextType.TEXT),
                    TextNode("another", TextType.BOLD),
                    ],
                new_nodes,
                )

    def test_delim_bold_multiword(self):
        node = TextNode(
                "This is text with a **bolded word** and **another**", TextType.TEXT
                )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded word", TextType.BOLD),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("another", TextType.BOLD),
                    ],
                new_nodes,
                )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word", TextType.TEXT),
                    ],
                new_nodes,
                )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
                [
                    TextNode("bold", TextType.BOLD),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    ],
                new_nodes,
                )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                    ],
                new_nodes,
                )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
                )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
                )
        self.assertListEqual(
                [
                    ("link", "https://boot.dev"),
                    ("another link", "https://blog.boot.dev"),
                    ],
                matches,
                )

    def test_split_images(self):
        node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
                )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode(
                        "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                        ),
                    ],
                new_nodes,
                )

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a 'code block' and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    ],
                new_nodes
                )

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                    ],
                )

    def test_block_to_block_type_heading_single_pound(self):
        md = "# This is a heading"
        blocks = markdown_to_blocks(md)
        heading = blocks[0]
        is_heading = block_to_block_type(heading)
        self.assertEqual(
                is_heading,
                BlockType.HEADING
        )

    def test_block_to_block_type_heading_multiple_pound(self):
        md = "###### This is a heading"
        blocks = markdown_to_blocks(md)
        heading = blocks[0]
        is_heading = block_to_block_type(heading)
        self.assertEqual(
                is_heading,
                BlockType.HEADING
        )

    def test_block_to_block_type_code(self):
        md = "```This is a code block```"
        blocks = markdown_to_blocks(md)
        code_block = blocks[0]
        is_code_block = block_to_block_type(code_block)
        self.assertEqual(
                is_code_block,
                BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        md = """
>I am a quote.
>So I am.
>Hey, me too!
"""
        blocks = markdown_to_blocks(md)
        quote_block = blocks[0]
        is_quote_block = block_to_block_type(quote_block)
        self.assertEqual(
                is_quote_block,
                BlockType.QUOTE
        )

    def test_block_to_block_type_ulist(self):
        md = """
- Bacon
- Ham
- Eggs
"""
        blocks = markdown_to_blocks(md)
        ulist_block = blocks[0]
        is_ulist_block = block_to_block_type(ulist_block)
        self.assertEqual(
                is_ulist_block,
                BlockType.UNORDERED_LIST
        )
    def test_block_to_block_type_olist(self):
        md = """
1. First comes love
2. Then comes marriage
3. Then comes a baby carriage
4. Then comes divorce and a new wife
"""
        blocks = markdown_to_blocks(md)
        olist_block = blocks[0]
        is_olist_block = block_to_block_type(olist_block)
        self.assertEqual(
                is_olist_block,
                BlockType.ORDERED_LIST
        )

if __name__ == "__main__":
    unittest.main()
