import typer
from typing import Optional

from pathlib import Path

app = typer.Typer()

path = "tests/step2/valid.json"
tokenized_list = []

index = 0


def is_number(num: str):
    try:
        float(num)
        return True
    except ValueError:
        return False


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
    task_types = ["None", "getting_string"]

    json_contents = open_json(path)
    in_string = False
    current_string = ""
    index = 0
    for token in json_contents:
        # print(token)
        if token == "{":
            tokenized_list.append({"LEFT_BRACE": None})
        elif token == "}":
            tokenized_list.append({"RIGHT_BRACE": None})
        elif token == "[":
            tokenized_list.append({"LEFT_BRACKET": None})
        elif token == "]":
            tokenized_list.append({"RIGHT_BRACKET": None})
        elif token == ":":
            tokenized_list.append({"COLON": None})
        elif token == ";":
            tokenized_list.append({"SEMI_COLON": None})
        elif token == ",":
            tokenized_list.append({"COMMA": None})
        elif token.lower() == "true":
            tokenized_list.append({"BOOLEAN": True})
        elif token.lower() == "false":
            tokenized_list.append({"BOOLEAN": False})
        elif is_number(token):
            tokenized_list.append({"INT": token})

        if token == '"' and not in_string:
            in_string = True
        elif token == '"' and in_string:
            in_string = False
            tokenized_list.append({"STRING": current_string})
            current_string = ""

        if in_string and token != '"':
            current_string += token

    # print(tokenized_list)
    return tokenized_list


def parse_object(token_list):
    parsed_object = {}

    return parsed_object


def parse_array(token_list):
    parsed_array = []
    return parsed_array


def parse_value(token_list):
    parsed_json = None
    for token in token_list:
        if parsed_json is None and token == "LEFT_BRACE":
            parsed_json = {}
            previous_token = token
        elif parsed_json is None and token == "LEFT_BRACKET":
            parsed_json = []
            previous_token = token

    return parsed_json, index


@app.command()
def parse_json(path: str = typer.Option(None, "-open", "-o", help="Path to JSON")):
    """
    Parses a json file
    """
    if len(tokenized_list) == 0:
        tokenize_json(path)
    print("Tokenized list")
    print(tokenized_list)

    parsed_json = parse_value(tokenized_list)

    print(type(parsed_json))
    print(parsed_json)
    return parsed_json


@app.command()
def xdc():
    print("xdc")


if __name__ == "__main__":
    app()
    # tokenize_json(path)
