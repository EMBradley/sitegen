"""
Provides functionality for converting markdown documents to blocks for further processing.
"""


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Splits the given text into markdown blocks.
    Blocks are delimited by two new lines.
    """
    blocks = markdown.split("\n\n")
    blocks = map(lambda block: block.strip(), blocks)
    blocks = filter(bool, blocks)

    return list(blocks)
