# Doc Note Untangler

<a href="https://pypi.org/project/doc_note_untangler/"><img alt="PyPI" src="https://img.shields.io/pypi/v/doc_note_untangler"></a>

A tiny tool for extracting special blocks from docstrings and embedding them in a static web page.

See an example [here][self-notes].

## Motivation

Good documentation can be invaluable in the long term, but it takes effort which can be difficult to justify in the short term.
Not all projects are expansive libraries or frameworks, often they're just small applications with just a couple of pieces of critical business logic.
In those cases especially it may be tempting to forgo external documentation, which will of course bite you right back when it comes to onboarding new people or having to explain a particular behavior to your stakeholders over and over again.

We have plenty of tools for building and hosting static pages and wikis from dedicated files but when it comes to documenting business logic, they require extreme vigilance to avoid discrepencies between docs and actual behavior.
Misleading docs are often worse than no docs at all.

To avoid accumulation of discrepencies over time, it helps to put your docs near the code itself, so the engineer who modifies it can quickly spot new inaccuracies in docs and fix them.

Module, class and function docstrings are a fine place for such docs, and this tool will let you easily define which parts of them may be relevant to external users and generate a static page for them.

## Details

When **not** to use this tool:
- You're documenting a library, framework or a complex application
- You're generating reference manuals for your api

When you **may** want to use this tool:
- Your application contains a several pieces of logic which should be documented externally

## Usage

``` sh
python -m doc_note_untangler.cli <directory>
```

### Examples

The notes extractracted from this very project are hosted at [github pages][self-notes].
You will find the relevant docstrings in the [source code][example-docstring]. 

### Configuration

The CLI application offers some basic configuration such as setting the source paths and output dir.
See `python -m doc_note_untangler.cli --help` for all options.

If you desire more complex customization, copypaste the source code into your own project and modify it at will.

[self-notes]: https://msladecek.github.io/doc_note_untangler/
[example-docstring]: https://github.com/msladecek/doc_note_untangler/blob/main/doc_note_untangler/build.py#L2
