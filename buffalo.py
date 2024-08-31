#!/usr/bin/env python3

import argparse
from FileHandler import FileHandler, LineByLineReadStrategy


def main():
    parser = argparse.ArgumentParser(
        description="Buffalo: tokenizador de archivos de texto conteniendo codigo de python"
    )

    # Definiendo un flag que requiere un valor

    parser.add_argument("-f", "--file", type=str, help="El nombre del archivo")
    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit(0)

    # Verificando si se proporcionó el archivo
    if args.file:
        path = args.file.strip()
        line_by_line_handler = FileHandler(path, LineByLineReadStrategy())
        print(line_by_line_handler.read())

    else:
        print("No se proporcionó ningún archivo.")


if __name__ == "__main__":
    main()
