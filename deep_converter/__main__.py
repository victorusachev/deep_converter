from deep_converter.main import FileWrapper, convert, flatten


def main():
    import argparse
    import os
    from pathlib import Path
    from pprint import pprint

    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        help='path to file that must be converted',
                        type=Path)

    args = parser.parse_args()

    paths = list()

    if args.path.is_dir():
        for root, dirs, files in os.walk(args.path):
            paths.extend(Path(root) / file for file in files)
    elif args.path.is_file():
        paths.append(args.path)

    for path in paths:
        res = tuple(convert(FileWrapper(path)))
        pprint(flatten(res), indent=4, width=200)


if __name__ == '__main__':
    main()
