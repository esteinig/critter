import typer
from pathlib import Path
from typing import Optional


app = typer.Typer(add_completion=False)


@app.command()
def birth_death_skyline(
    reference: Path = typer.Argument(..., help="Reference used in alignment in FASTA format"),
    alignment: Path = typer.Argument(..., help="Alignment of variant calls in FASTA format"),
    dates: Path = typer.Argument(..., help="Date file, tab-separated `name` and `date` headers")
):
    """
    Birth death skyline model
    """

