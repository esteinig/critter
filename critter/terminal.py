import typer

app = typer.Typer()


def model_loader(ctx):
    pass


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")
