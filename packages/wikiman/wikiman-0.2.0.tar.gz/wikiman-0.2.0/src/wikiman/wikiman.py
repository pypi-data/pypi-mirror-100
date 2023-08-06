"""Generate wiki navigation links in the sidebar and footer of each page."""

import itertools
from pathlib import Path

import fire
from markdown import Markdown

ROOT_DIRNAME = "wiki"
ROOT_PAGE_NAME = "Home.md"
ROOT_PAGE = Path(ROOT_DIRNAME) / ROOT_PAGE_NAME
PAGE_PATTERN = "[!_]*.md"

ROOT = Path(ROOT_DIRNAME)
WIKI_ROOT = "https://github.com/blakeNaccarato/python-challenges/wiki"

SIDEBAR_FILENAME = "_Sidebar.md"
FOOTER_FILENAME = "_Footer.md"

# Glyphs to place in the footer next to "Up", "Prev", and "Next" navigation links.
NAV_HEAD = ("Up: ", "Prev: ", "Next: ")
# Heading levels indicated by number of "#" in sequence. Changes header size.
MD_HEAD = "# "
# Two newlines signifies a paragraph break in Markdown.
MD_NEWLINE = "  \n"
# Workaround. Markdown converts sequential whitespace (other than \n) to single spaces.
MD_TAB = "&nbsp;" * 4

# Width of the number to prepend to directories
WIDTH = 2


def main():
    """Runs only if this file is run directly, rather than imported."""

    fire.Fire(
        {
            "up": update_navigation,
            "add": add_page,
        }
    )


# * -------------------------------------------------------------------------------- * #
# * CLI


def update_navigation():
    """Update sidebars and footers."""

    pages = get_descendants(ROOT)
    for page in pages:

        # Write the tree of nearby pages and the TOC for this page into the sidebar
        tree = get_tree(page)
        toc = get_toc(page)
        sidebar_text = MD_NEWLINE.join(
            [f"{MD_HEAD}Directory", tree, f"{MD_HEAD}Contents", toc]
        )
        sidebar = page.parent / SIDEBAR_FILENAME
        with open(sidebar, "w") as file:
            file.write(sidebar_text)

        # Write relative navigation links into the footer
        nav = get_relative_nav(page, NAV_HEAD)
        footer = page.parent / FOOTER_FILENAME
        with open(footer, "w") as file:
            file.write(nav)


def add_page(name: str, at_name: str, relative_to: str = "under"):
    """Add a new page after or under the specified page."""

    if relative_to != "under" and relative_to != "after":
        raise ValueError("Third argument must be either 'under' or 'after'.")

    at_page = get_page(at_name)

    if at_page == ROOT_PAGE and relative_to == "after":
        raise ValueError("Can't add sibling to root.")

    if relative_to == "under":
        at_dir = at_page.parent
        position = len(get_children(at_page))

    elif relative_to == "after":

        parent = get_parent(at_page)
        at_dir = parent.parent

        # Get the siblings that will come after the new page
        siblings = get_siblings(at_page)
        position = siblings.index(at_page) + 1
        siblings_after = siblings[position:]

        # Shift sibling directory numbering to accomdate the new page
        for sibling in siblings_after:
            sibling_dir = sibling.parent
            sibling_position = int(sibling_dir.name.split(" ")[0])
            sibling_position += 1
            new_dir_name = get_dir_name(get_human_name(sibling.stem), sibling_position)
            new_dir = at_dir / new_dir_name
            sibling_dir.rename(new_dir)

    make_page(name, at_dir, position)


# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


def get_page(name: str) -> Path:
    """Get a page given its name."""

    pages = get_descendants(ROOT)
    page_names = [get_human_name(page.stem).lower() for page in pages]
    page_location = page_names.index(name.lower())
    return pages[page_location]


def make_page(name: str, at_dir: Path, position: int):
    """Make a new page in the wiki."""

    page_dir = at_dir / get_dir_name(name, position)
    page_dir.mkdir()

    new_page = page_dir / get_md_name(name)
    new_page.touch()


# * -------------------------------------------------------------------------------- * #
# * NAVIGATION


def get_tree(page: Path) -> str:
    """Get Markdown links for the tree of pages near a page."""

    # Start the tree at root or with the page and its siblings
    if page == ROOT_PAGE:
        # Tree is a list of just the root page
        tree = [bold_md(get_page_link(page))]
        page_idx = 0
    else:
        siblings = get_siblings(page)
        tree = [get_page_link(page) for page in siblings]
        page_idx = siblings.index(page)
        tree[page_idx] = bold_md(tree[page_idx])

    # Insert child links below the page
    children = get_children(page)
    child_links = [get_page_link(page) for page in children]
    tree = insert_subtree(subtree=child_links, tree=tree, index=page_idx)

    # Only worry about parents if it's not the root page
    if page != ROOT_PAGE:

        parent = get_parent(page)

        if parent == ROOT_PAGE:
            # Insert the working tree below the root page
            parent_links = [get_page_link(parent)]
            parent_idx = 0
            tree = insert_subtree(subtree=tree, tree=parent_links, index=parent_idx)
        else:
            # Insert the working tree below the parent page in the list of parents
            parents = get_siblings(parent)
            parent_links = [get_page_link(page) for page in parents]
            parent_idx = parents.index(parent)
            tree = insert_subtree(subtree=tree, tree=parent_links, index=parent_idx)

    return MD_NEWLINE.join(tree)


def insert_subtree(subtree: list[str], tree: list[str], index: int):
    """Insert a subtree into a tree after the specified index."""

    index += 1  # To insert *after* the specified index.

    subtree = [MD_TAB + str(i) for i in subtree]
    tree = list(itertools.chain(tree[:index], subtree, tree[index:]))
    return tree


def get_toc(page: Path) -> str:
    """Get the table of contents for a page."""

    toc_list: list[str] = []
    page_url = get_page_url(page)

    with open(page) as file:
        content = file.read()
        md = Markdown(extensions=["toc"])
        md.convert(content)

    for token in md.toc_tokens:  # type: ignore  # pylint: disable=no-member
        token_id = token["id"]
        name = token["name"]
        link = get_md_link(name, f"{page_url}#{token_id}")
        toc_list.append(link)

    toc = MD_NEWLINE.join(toc_list)

    return toc


def get_relative_nav(page: Path, nav_head: tuple[str, str, str]) -> str:
    """Get the parent, previous, and next Markdown links."""

    relative_nav: list[str] = []

    nearest_family = get_nearest_family(page)
    (parent, prev_sibling, next_sibling) = nearest_family

    # Get parent link for any page except for Home
    if page == ROOT_PAGE:
        parent_link = None
    else:
        parent_link = get_page_link(parent)
        relative_nav.append(nav_head[0] + parent_link)

    # Get previous link for pages with a different previous sibling than their parent
    if parent == prev_sibling:
        prev_link = None
    else:
        prev_link = get_page_link(prev_sibling)
        relative_nav.append(nav_head[1] + prev_link)

    # Get next link
    next_link = get_page_link(next_sibling)
    relative_nav.append(nav_head[2] + next_link)

    nav = MD_TAB.join(relative_nav)

    return nav


# * -------------------------------------------------------------------------------- * #
# * MARKDOWN


def bold_md(text: str) -> str:
    """Make text bold in Markdown format."""

    return f"**{text}**"


def get_page_link(page: Path) -> str:
    """Get a link to a page in Markdown format."""

    return get_md_link(get_human_name(page.stem), get_page_url(page))


def get_md_link(text: str, link: str) -> str:
    """Get a link in Markdown format."""

    return f"[{text}]({link})"


def get_page_url(page: Path) -> str:
    """Get the URL for a page."""

    return f"{WIKI_ROOT}/{page.stem}"


# * -------------------------------------------------------------------------------- * #
# * STRINGS


def get_dir_name(name: str, index: int) -> str:
    """Get the name for the directory containing a page in the file structure."""

    return str(index).zfill(WIDTH) + " " + get_human_name(name)


def get_human_name(name: str) -> str:
    """Get the human-readable name for a page, as in Markdown."""

    return name.replace("-", " ")


def get_md_name(name: str) -> str:
    """Get the name for a `*.md` page in the file structure."""

    return name.replace(" ", "-") + ".md"


# * -------------------------------------------------------------------------------- * #
# * FAMILY


def get_descendants(page: Path) -> list[Path]:
    """Get a page and all of its descendants."""

    return list(page.glob(f"**/{PAGE_PATTERN}"))


def get_nearest_family(page: Path) -> tuple[Path, Path, Path]:
    """Get a page's parent and its nearest siblings."""

    parent = get_parent(page)
    siblings = get_siblings(page)

    if page.name == ROOT_PAGE_NAME:
        prev_sibling = page  # The Home page is its own previous sibling
        next_sibling = siblings[0]  # The next page is its next sibling
    else:
        page_position = siblings.index(page)

        # Get the previous sibling
        is_first_child = page_position == 0
        if is_first_child:
            prev_sibling = get_parent(page)
        else:
            prev_sibling = siblings[page_position - 1]

        # Get the next sibling
        any_subpages = any(item.is_dir() for item in page.parent.iterdir())
        is_last_child = page_position == len(siblings) - 1
        if any_subpages:
            # Make a page with children have its first child as a sibling
            first_child_dir = [p for p in page.parent.iterdir() if p.is_dir()][0]
            first_child = list(first_child_dir.glob(PAGE_PATTERN))[0]
            next_sibling = first_child
        elif is_last_child:
            # Make the next sibling of the parent also the next sibling of this page
            (*_, next_sibling_of_parent) = get_nearest_family(parent)
            next_sibling = next_sibling_of_parent
        else:
            next_sibling = siblings[page_position + 1]

    return parent, prev_sibling, next_sibling


def get_siblings(page: Path) -> list[Path]:
    """Get a page and its siblings."""

    parent = get_parent(page)
    children_of_parent = get_children(parent)
    siblings = children_of_parent
    return siblings


def get_children(page: Path) -> list[Path]:
    """Get the children of a page."""

    parent_directory = page.parent
    return list(parent_directory.glob(f"*/{PAGE_PATTERN}"))


def get_parent(page: Path) -> Path:
    """Get the parent of a page."""

    if page == ROOT_PAGE:
        # Make the Home page its own parent
        parent = page

    else:
        # Make the page in the parent directory its parent
        page_directory = page.parent
        parent_directory = page_directory.parent
        # If each page has its own directory, glob should get only one page
        parent = list(parent_directory.glob(PAGE_PATTERN))[0]

    return parent


# * -------------------------------------------------------------------------------- * #
# * RUN MAIN

if __name__ == "__main__":
    main()
