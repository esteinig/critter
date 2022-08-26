import typer
from typing import Optional, List
from critter.critter import Critter
from critter.config import load_config
from pandas import concat
from pathlib import Path
from critter.diagnostic import PosteriorDiagnostic
from critter.plots import plot_equal_re_intervals, plot_sample_date_distribution, plot_bdsky_posterior_summary
from critter.utils import get_date_range, dates_from_fasta

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
    output: Optional[Path] = typer.Option("model.xml", help="XMl model output file for BEAST 2.6+"),
    tree_log: Optional[Path] = typer.Option('tree.log', help="Tree log file [sample_every intervals]"),
    posterior_log: Optional[Path] = typer.Option('posterior.log', help="Posterior log file [sample_every intervals]"),
    sample_every: Optional[int] = typer.Option(1000, help="Length of sample intervals for posterior and trees"),
    chain_length: Optional[int] = typer.Option(100000000, help="Number of steps in the Markov chain"),
    chain_type: Optional[str] = typer.Option('default', help="MCMC (default) or coupled MCMC (mcmcmc)"),
    chain_number: Optional[int] = typer.Option(4, help="Number of chains in coupled MCMC"),
    multiple: Optional[int] = typer.Option(1, help="Create multiple copies for independent runs"),
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
                ambiguities=ambiguities,
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
        plot_equal_re_intervals(posterior_diagnostic=diagnostic, output=plot_file, last_sample=last)


@bdsky_app.command()
def posterior_dist(
    posterior_log: Path = typer.Argument(..., help="Posterior log file of model run"),
    prior_log: Optional[Path] = typer.Option(None, help="Log of same model run with sampling from prior"),
    output: Optional[Path] = typer.Option('posterior.png', help="Output file for posterior summary"),
    size: Optional[str] = typer.Option('14,10', help="Output plot sizes"),
):
    """
    Create a plot of model parameter posterior density distributions
    """
    post = PosteriorDiagnostic(posterior_log)

    # matching log, sampled from prior
    if prior_log is not None:
        prior = PosteriorDiagnostic(prior_log)
    else:
        prior = None

    plot_file = post.log.with_suffix(".png")
    plot_bdsky_posterior_summary(
        posterior=post, posterior_prior=prior, output=output if output else plot_file, size=size
    )


@utils_app.command()
def date_range(
    dates: Path = typer.Argument(..., help="Date file, no header, tab-seperated, name [0] dates [1]"),
    datefmt: Optional[bool] = typer.Option(False, help="Dates in date file are in format: DD/MM/YYYY"),
    header: Optional[bool] = typer.Option(False, help="Header is present"),
):
    """
    Output the date range for a date file
    """

    if dates.suffix == ".log":
        max_date, min_date, delta, counts = get_date_range(log_file=dates)
    else:
        max_date, min_date, delta, counts = get_date_range(file=dates, sep='\t', datefmt=datefmt, header=header)
    print(f"{min_date} - {max_date} [{delta}]")
    print(counts)


@utils_app.command()
def date_density(
    dates: List[Path] = typer.Argument(..., help="Date file, no header, tab-seperated, name [0] dates [1]"),
    datefmt: Optional[bool] = typer.Option(False, help="Dates in date file are in format: DD/MM/YYYY"),
    equal_slices: Optional[int] = typer.Option(0, help="Vertical lines denoting equal slice change points"),
    output: Path = typer.Option("date_density.png", help="Output plot file for date distributions")
):
    """
    Output a plot of the date distributions 
    """

    plot_sample_date_distribution(date_files=dates, datefmt=datefmt, equal_slices=equal_slices, output=output)


@utils_app.command()
def date_from_fasta(
    fasta: Path = typer.Argument(..., help="Fasta file with dates in sequence identifier"),
    date_idx: int = typer.Option(default=2, help="Sequence date index in sequence identifier"),
    datefmt: Optional[bool] = typer.Option(False, help="Dates are in format: DD/MM/YYYY"),
    output: Path = typer.Option("dates.tsv", help="Output plot file for date distributions")
):
    """
    Output a plot of the date distributions
    """

    dates_from_fasta(fasta=fasta, date_file=output, date_idx=date_idx, datefmt=datefmt)

