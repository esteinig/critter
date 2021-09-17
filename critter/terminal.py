import typer
from pathlib import Path
from typing import Optional


app = typer.Typer(add_completion=False)


@app.command()
def birth_death_skyline(
    reference: Path = typer.Argument(..., help="Reference used in alignment (FASTA)"),
    alignment: Path = typer.Argument(..., help="Alignment of variant calls (FASTA)"),
    dates: Path = typer.Argument(..., help="Tab-separated, name and date, no header")
):
    """
    Birth death skyline model
    """

