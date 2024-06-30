# pylint: disable=unspecified-encoding
"""
`sitegen` is a static site generation tool that converts markdown to html.
This package was created as part of the author's completion of Boot.dev's
backend developer course.
"""

from os import curdir, listdir, makedirs, mkdir, path
from shutil import copy, rmtree

from markdown_blocks import extract_title, markdown_to_html_node


def main():
    """Entry point for `sitegen`"""
    print("Generating pages...")
    copy_static()
    generate_pages_recursive("content", "public", "template.html")
    print("Complete!")


def generate_pages_recursive(
    content_dir_path: str, dst_dir_path: str, template_path: str
):
    """
    Recursively walks through the directory at `content_dir_path`, generating an html file
    from each markdown file it finds, and places them all in `dst_dir_path`
    """
    assert path.exists(content_dir_path)

    for item in listdir(content_dir_path):
        item_path = path.join(content_dir_path, item)
        dst_path = path.join(dst_dir_path, item)
        if path.isfile(item_path):
            if item_path.endswith(".md"):
                dst_path = dst_path.replace(".md", ".html")
                generate_page(item_path, dst_path, template_path)
        else:
            generate_pages_recursive(item_path, dst_path, template_path)


def generate_page(src_path: str, dst_path: str, template_path: str):
    """
    Creates an html file at `dst_path` from an html template at
    `template_path` and a markdown file at `src_path`
    """
    print(f"Generating page from {src_path} to {dst_path} using {template_path}...")

    with open(src_path, "r") as md_file:
        markdown = md_file.read()
    with open(template_path, "r") as template_file:
        template_html = template_file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    result = template_html.replace("{{ Title }}", title).replace("{{ Content }}", html)

    if not path.exists(path.dirname(dst_path)):
        makedirs(path.dirname(dst_path))

    with open(dst_path, "w") as dst_file:
        dst_file.write(result)


def copy_static():
    """
    Deletes the contents of the `public` directory,
    then copies the contents of `static` into `public`
    """
    static = path.join(curdir, "static")
    public = path.join(curdir, "public")

    rmtree(public)
    copy_dir(static, public)


def copy_dir(src: str, dst: str):
    """
    Copies the contents of the `src` directory into the `dst` directory.
    Files in `dst` that have the same name as a file in `src` are overwritten.
    """
    assert path.exists(src)
    if not path.exists(dst):
        mkdir(dst)

    for item in listdir(src):
        item_path = path.join(src, item)
        if path.isfile(item_path):
            copy(item_path, dst)
        else:
            dst_item_path = path.join(dst, item)
            mkdir(dst_item_path)
            copy_dir(item_path, dst_item_path)


if __name__ == "__main__":
    main()
