"""
Provides functionality for converting markdown documents to blocks for further processing.
"""

from enum import Enum
import re

BlockType = Enum(
    "BlockType",
    ["Paragraph", "Heading", "Code", "Quote", "UnorderedList", "OrderedList"],
)


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


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Splits the given text into markdown blocks.
    Blocks are delimited by two new lines.
    """
    blocks = markdown.split("\n\n")
    blocks = map(lambda block: block.strip(), blocks)
    blocks = filter(lambda block: block != "", blocks)

    return list(blocks)
