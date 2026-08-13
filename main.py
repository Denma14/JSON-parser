import typer
from typing import Optional

from pathlib import Path

app = typer.Typer()


@app.command()
def open_json(path: str = typer.Option(None, "-open", "-o", help="Path to JSON")):
    if path is not None:
        with open(path, "rt") as f:
            json_contents = f.read()
            total_char = len(json_contents)
            print(json_contents)
            print(total_char)
            if total_char == 0:
                typer.echo("INVALID JSON")
                raise typer.Exit(1)
    else:
        typer.echo("No path provided")


@app.command()
def xdc():
    print("xdc")


if __name__ == "__main__":
    app()
