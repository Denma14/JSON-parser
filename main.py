import typer
from typing import Optional

from pathlib import Path

app = typer.Typer()


@app.command()
def open_json(path: str = typer.Option(None, "-open", "-o", help="Path to JSON")):
    """
    Opens the json
    """
    if path is not None:
        with open(path, "rt") as f:
            json_contents = f.read()
            total_char = len(json_contents)
            # print(json_contents)
            # print(total_char)
            if total_char == 0:
                typer.echo("INVALID JSON")
                raise typer.Exit(1)
                return "{}"
            return json_contents
    else:
        typer.echo("No path provided")


@app.command()
def tokenize_json(path: str = typer.Option(None, "-open", "-o", help="Path to JSON")):
    """
    Tokenize the Jason
    """
    json_contents = open_json(path)
    tokenized_list = []
    for token in json_contents:
        print(token)
        if token == "{":
            tokenized_list.append("LEFT_BRACE")
        elif token == "}":
            tokenized_list.append("RIGHT_BRACE")
        elif token == "[":
            tokenized_list.append("LEFT_BRACKET")
        elif token == "]":
            tokenized_list.append("RIGHT_BRACKET")
        elif token == '"':
            ...
    print(tokenized_list)
    return tokenized_list


@app.command()
def parse_json(path: str = typer.Option(None, "-open", "-o", help="Path to JSON")):
    """
    Parses a json file
    """
    tokenized_list = tokenize_json(path)
    parsed_json = None
    for token in tokenized_list:
        if parsed_json is None and token == "LEFT_BRACE":
            parsed_json = {}
        elif parsed_json is None and token == "LEFT_BRACKET":
            parsed_json = []
    print(type(parsed_json))
    print(parsed_json)
    return parsed_json


@app.command()
def xdc():
    print("xdc")


if __name__ == "__main__":
    app()
