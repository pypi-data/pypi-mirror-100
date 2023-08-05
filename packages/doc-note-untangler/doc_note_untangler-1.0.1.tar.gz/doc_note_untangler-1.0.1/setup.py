# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doc_note_untangler']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.4,<4.0.0', 'Pygments>=2.8.1,<3.0.0', 'md-mermaid>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'doc-note-untangler',
    'version': '1.0.1',
    'description': 'Untangle special markdown blocks from docstrings and assemble them into a static webpage.',
    'long_description': '# Doc Note Untangler\n\n<a href="https://pypi.org/project/doc_note_untangler/"><img alt="PyPI" src="https://img.shields.io/pypi/v/doc_note_untangler"></a>\n\nA tiny tool for extracting special blocks from docstrings and embedding them in a static web page.\n\nSee an example [here][self-notes].\n\n## Motivation\n\nGood documentation can be invaluable in the long term, but it takes effort which can be difficult to justify in the short term.\nNot all projects are expansive libraries or frameworks, often they\'re just small applications with just a couple of pieces of critical business logic.\nIn those cases especially it may be tempting to forgo external documentation, which will of course bite you right back when it comes to onboarding new people or having to explain a particular behavior to your stakeholders over and over again.\n\nWe have plenty of tools for building and hosting static pages and wikis from dedicated files but when it comes to documenting business logic, they require extreme vigilance to avoid discrepencies between docs and actual behavior.\nMisleading docs are often worse than no docs at all.\n\nTo avoid accumulation of discrepencies over time, it helps to put your docs near the code itself, so the engineer who modifies it can quickly spot new inaccuracies in docs and fix them.\n\nModule, class and function docstrings are a fine place for such docs, and this tool will let you easily define which parts of them may be relevant to external users and generate a static page for them.\n\n## Details\n\nWhen **not** to use this tool:\n- You\'re documenting a library, framework or a complex application\n- You\'re generating reference manuals for your api\n\nWhen you **may** want to use this tool:\n- Your application contains a several pieces of logic which should be documented externally\n\n## Usage\n\n``` sh\npython -m doc_note_untangler.cli <directory>\n```\n\n### Examples\n\nThe notes extractracted from this very project are hosted at [github pages][self-notes].\nYou will find the relevant docstrings in the [source code][example-docstring]. \n\n### Configuration\n\nThe CLI application offers some basic configuration such as setting the source paths and output dir.\nSee `python -m doc_note_untangler.cli --help` for all options.\n\nIf you desire more complex customization, copypaste the source code into your own project and modify it at will.\n\n[self-notes]: https://msladecek.github.io/doc_note_untangler/\n[example-docstring]: https://github.com/msladecek/doc_note_untangler/blob/main/doc_note_untangler/build.py#L2\n',
    'author': 'msladecek',
    'author_email': 'martin.sladecek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/msladecek/doc_note_untangler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
