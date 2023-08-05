import argparse
import sys
from pathlib import Path

from pygments.formatters import get_formatter_by_name

from doc_note_untangler.build import build_page, load_notes


def main(argv):
    parser = argparse.ArgumentParser(prog="doc_note_untangler.cli")
    parser.add_argument("source_paths", type=Path, metavar="source_path", nargs="+")
    parser.add_argument("--output_dir", type=Path, default="_docs")
    parser.add_argument("--pygments_style", type=str, default="default")
    parser.add_argument("--project_title", type=str, default="Docstring Notes")
    args = parser.parse_args(argv)

    notes = sorted(load_notes(args.source_paths), key=(lambda note: note["file_path"]))

    args.output_dir.mkdir(parents=True, exist_ok=True)

    formatter = get_formatter_by_name("html", style=args.pygments_style)
    with open(args.output_dir / "pygments_styles.css", "w") as cssfile:
        cssfile.write(formatter.get_style_defs(".codehilite"))

    with open(args.output_dir / "index.html", "w") as htmlfile:
        htmlfile.write(build_page(notes, project_title=args.project_title))


if __name__ == "__main__":
    main(sys.argv[1:])
