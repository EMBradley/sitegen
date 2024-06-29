"""
Provides functionality for converting markdown documents to blocks for further processing.
"""

import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes

BlockType = Enum(
    "BlockType",
    ["Paragraph", "Heading", "Code", "Quote", "UnorderedList", "OrderedList"],
)


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Converts a `str` representing a markdown document
    into an `HTMLNode` for converting to html
    """

    def text_to_leaf_nodes(text: str) -> list[LeafNode]:
        return [node.to_html_node() for node in text_to_textnodes(text)]

    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        match get_block_type(block):
            case BlockType.Paragraph:
                node = ParentNode("p", text_to_leaf_nodes(block))

            case BlockType.Heading:
                hashes, content = block.split(" ", 1)
                node = ParentNode(f"h{len(hashes)}", text_to_leaf_nodes(content))

            case BlockType.Code:
                content = block[3:-3]
                node = ParentNode(
                    "per", [ParentNode("code", text_to_leaf_nodes(content))]
                )

            case BlockType.Quote:
                lines = block.split("\n")
                content = "\n".join(map(lambda line: line.removeprefix("> "), lines))
                node = ParentNode("blockquote", text_to_leaf_nodes(content))

            case BlockType.UnorderedList:
                lines = block.split("\n")
                list_items = []
                for line in lines:
                    line_content = line[2:]
                    line_nodes = text_to_leaf_nodes(line_content)
                    list_items.append(ParentNode("li", line_nodes))
                node = ParentNode("ul", list_items)

            case BlockType.OrderedList:
                lines = block.split("\n")
                list_items = []
                for i, line in enumerate(lines):
                    line_content = line.removeprefix(f"{i + 1}. ")
                    line_nodes = text_to_leaf_nodes(line_content)
                    list_items.append(ParentNode("li", line_nodes))
                node = ParentNode("ol", list_items)

            case _:
                raise ValueError("Invalid block")

        nodes.append(node)

    return ParentNode("div", nodes)


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Splits the given text into markdown blocks.
    Blocks are delimited by two new lines.
    """
    blocks = markdown.split("\n\n")
    blocks = map(lambda block: block.strip(), blocks)
    blocks = filter(lambda block: block != "", blocks)

    return list(blocks)


def get_block_type(block: str) -> BlockType:
    """
    Determines the block type of a markdown block
    """
    if re.match(r"^#{1,6} .*", block):
        return BlockType.Heading

    lines = block.split("\n")
    if lines and re.match(r"^```", lines[0]) and re.search(r"```$", lines[-1]):
        return BlockType.Code
    if all(re.match(r"^> ", line) for line in lines):
        return BlockType.Quote
    if all(re.match(r"^[*-] ", line) for line in lines):
        return BlockType.UnorderedList
    if all(
        re.match(r"^" + str(i + 1) + r"\. .*", line) for (i, line) in enumerate(lines)
    ):
        return BlockType.OrderedList

    return BlockType.Paragraph
