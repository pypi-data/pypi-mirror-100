"""Docstring note extractor & html page builder.
::: doc-note Example note
    Define special `doc-note` blocks in docstrings and they will be rendered here.
    Markdown is supported.

    You can even do diagrams with [mermaid](https://mermaid-js.github.io/mermaid/#/):
    ```mermaid
    graph LR
        a --> b
        a --> c
        b --> c
    ```

    Was produced from:
    ```
    ::: doc-note Example note
        Define special `doc-note` blocks in docstrings and they will be rendered here.
        Markdown is supported.

        You can even do diagrams with [mermaid](https://mermaid-js.github.io/mermaid/#/):
        ```mermaid
        graph LR
            a --> b
            a --> c
            b --> c
        ```
    ```

(This part of the docsting will not be part of the note because it's outside of the doc-note indented block.)


::: doc-note Another Example note
    There can be multiple notes in a single docstring.

    Here's some cool python code and a table as a bonus:

    ```python
    from functools import reduce
    from operator import mul

    def factorial(n):
        return reduce(mul, range(1, n + 1))
    ```

    | ascii | nato    | talon  |
    | ---   | ---     | ---    |
    | W     | whiskey | whale  |
    | Q     | quebec  | quench |
"""
import ast
import os

import markdown


def iter_docstrings(root):
    if isinstance(root, ast.ClassDef):
        yield root.name, ast.get_docstring(root)
        yield from iter_docstrings(root.body)
    elif isinstance(root, ast.Module):
        yield None, ast.get_docstring(root)
        yield from iter_docstrings(root.body)
    else:
        for node in root:
            if isinstance(node, ast.FunctionDef):
                yield node.name, ast.get_docstring(node)
            elif isinstance(node, ast.AsyncFunctionDef):
                yield node.name, ast.get_docstring(node)
            elif isinstance(node, ast.ClassDef):
                yield from iter_docstrings(node)


def iter_files(root_path):
    for current, _, files in os.walk(root_path):
        for file_ in files:
            if file_.endswith(".py"):
                yield os.path.join(current, file_)


def iter_notes(docstring):
    lines = docstring.splitlines()
    note_lines = None
    attrs = {}

    def _flush():
        nonlocal note_lines, attrs
        title = attrs.get("title")
        id_ = attrs.get("id", title)
        yield {"id": id_, "title": title, "content": "\n".join(note_lines)}
        note_lines = []
        attrs = {}

    for line in lines:
        if line.startswith("::: doc-note"):
            _, __, title = line.partition("::: doc-note")
            if note_lines is not None:
                yield from _flush()
            else:
                note_lines = []
            attrs = {"title": title}
        else:
            if line != "" and not line.startswith("   ") and note_lines is not None:
                yield from _flush()
                note_lines = None
            elif note_lines is not None:
                note_lines.append(line[4:])

    if note_lines is None:
        yield from _flush()


def load_notes(source_paths):
    notes = []
    for source_path in source_paths:
        for file_path in iter_files(source_path):
            with open(file_path) as f:
                module = ast.parse(f.read())
                for obj_name, docstring in iter_docstrings(module):
                    if docstring is None:
                        continue

                    for note in iter_notes(docstring):
                        notes.append({"file_path": file_path, "obj_name": obj_name, **note})
    return notes


def build_page(notes, *, project_title):
    """Compose an html document with all the notes.

    ::: doc-note Building the page
        Notes are untangled from source files and rendered as markdown.
        Diagrams are rendered by [mermaid.js](https://mermaid-js.github.io/mermaid/#/).
        Page is styled with [mvp.css](https://andybrewer.github.io/mvp/).

        It looks a bit like this:

        ```mermaid
        flowchart LR;
            subgraph "source files"
                src1.py
                src2.py
                other_src.py[....py]
            end

            untangler([untangler])

            src1.py --> untangler
            src2.py --> untangler
            other_src.py --> untangler

            subgraph "external resources"
                mermaid([mermaid.js])
                mvp([mvp.css])
                cdn((cdn))
                mermaid --> cdn
                mvp --> cdn
            end

            untangler --> index.html
            cdn --> index.html
        ```
    """
    page_template = """<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="https://unpkg.com/mvp.css">
    <link rel="stylesheet" href="./pygments_styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/8.9.2/mermaid.min.js"></script>
    {extra_css}
    <title>{project_title}</title>
  </head>
  <body>
    <main>
      <h1>Notes</h1>
      {table_of_contents}
      <hr>
      {page_body}
    </main>
  </body>
</html>"""

    note_template = """
    <div>
        <h2>{title}</h2>
        {content}
    </div>
    """

    css = """
    <style>
    pre > span > code {
        background: white;
        border: 1px solid black;
    }
    </style>
    """

    table_of_contents_container_template = """
    <div>
      <h2>Contents</h2>
      <ul>
        {table_of_contents_items}
      </ul>
    </div>
    """

    table_of_contents_item = """
    <li><a href="#{id}">{title}</a></li>
    """

    md = markdown.Markdown(
        extensions=["fenced_code", "codehilite", "md_mermaid", "tables"],
        extension_configs={"codehilite": {"guess_lang": False}},
    )
    for note in notes:
        note["content"] = md.convert(note["content"])

    return page_template.format(
        project_title=project_title,
        extra_css=css,
        page_body="\n<hr>\n".join(note_template.format(**note) for note in notes),
        table_of_contents=table_of_contents_container_template.format(
            table_of_contents_items="\n".join(
                table_of_contents_item.format(**note) for note in notes if "id" in note
            )
        ),
    )
