import typer
from typing import Optional, List
from critter.critter import Critter
from critter.config import load_config
from pandas import concat
from pathlib import Path
from critter.diagnostic import PosteriorDiagnostic
from critter.plots import plot_re_intervals
from critter.utils import get_date_range

app = typer.Typer(add_completion=False)

bdsky_app = typer.Typer()
app.add_typer(bdsky_app, name="bdsky")


utils_app = typer.Typer()
app.add_typer(utils_app, name="utils")

@bdsky_app.command()
def model(
    config: Path = typer.Option(..., help="Model config file"),
    alignment: Path = typer.Option(..., help="Alignment file"),
    dates: Path = typer.Option(..., help="Date file, no header, tab-seperated, name [0] dates [1]"),
    output: Optional[Path] = typer.Option("model.xml", help="XMl model output file for BEAST"),
    tree_log: Optional[Path] = typer.Option('tree.log', help="Tree log file [sample_every intervals]"),
    posterior_log: Optional[Path] = typer.Option('posterior.log', help="Posterior log file [sample_every intervals]"),
    sample_every: Optional[int] = typer.Option(1000, help="Length of sample intervals for posterior and trees"),
    chain_length: Optional[int] = typer.Option(100000000, help="Number of steps in the Markov chain"),
    chain_type: Optional[str] = typer.Option('default', help="MCMC (default) or coupled MCMC (mcmcmc)"),
    chain_number: Optional[int] = typer.Option(4, help="Number of chains in coupled MCMC"),
    multiple: Optional[int] = typer.Option(1, help="Multiple copies for independent chain runs"),
    ambiguities: Optional[bool] = typer.Option(False, help="Allow ambiguous nucleotide sites in alignment (any)"),
    datefmt: Optional[bool] = typer.Option(False, help="Dates in date file are in format: DD/MM/YYYY")
):
    """
    Create a birth death skyline model from config file
    """
    
    critter_config = load_config(yaml_file=config)

    for i in range(multiple):
        critter_model = critter_config.get_model(
            critter=Critter(
                date_file=dates,
                alignment_file=alignment,
                tree_log=tree_log,
                posterior_log=posterior_log,
                chain_length=chain_length,
                sample_every=sample_every,
                chain_type=chain_type,
                chain_number=chain_number,
                allow_ambiguities=ambiguities,
                datefmt=datefmt
            )
        )
        if multiple > 1:
            indexed_output = output.with_suffix(f"_{i}{output.suffix}")
            critter_model.render(xml_file=indexed_output)
        else:
            critter_model.render(xml_file=output)

@bdsky_app.command()
def summary(
    logs: List[Path],
    output: Optional[Path] = typer.Option('summary.tsv', help="Output file for posterior summary")
):
    """
    Create a posterior summary from log files
    """


    diagnostics = [PosteriorDiagnostic(log) for log in logs]
    diagnostic_summary = concat([d.summary for d in diagnostics])
    diagnostic_summary.to_csv(output, sep='\t', index=False)

@bdsky_app.command()
def re_intervals(
    logs: List[Path],
    last: float = typer.Option(None, help="Last sample date (float)")
):
    """
    Create a plot of Re estimates (mean, 95% HPD) 
    """

    diagnostics = [PosteriorDiagnostic(log) for log in logs]

    for diagnostic in diagnostics:
        plot_file = diagnostic.log.with_suffix(".png")
        plot_re_intervals(posterior_diagnostic=diagnostic, output=plot_file, last_sample=last)


@utils_app.command()
def date_range(
    dates: Path = typer.Argument(..., help="Date file, no header, tab-seperated, name [0] dates [1]"),
    datefmt: Optional[bool] = typer.Option(False, help="Dates in date file are in format: DD/MM/YYYY")
):
    """
    Output the date range for a date file
    """

    max_date, min_date, delta = get_date_range(file=dates, sep='\t', datefmt=datefmt)

    print(f"{min_date} - {max_date} [{delta}]")