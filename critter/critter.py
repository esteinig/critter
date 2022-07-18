import jinja2
from pathlib import Path
from pyfastx import Fasta
from critter.utils import get_float_dates, NULL
from critter.errors import CritterError
import datetime

class Critter:

    def __init__(
        self,
        date_file: Path,
        alignment_file: Path,
        reference_file: Path = None,
        tree_log: Path = Path('tree.log'),
        posterior_log: Path = Path('posterior.log'),
        sample_every: int = 1000,
        chain_length: int = 100000,
        chain_type: str = 'default',
        chain_number: int = 4,
        ambiguities: bool = False,
        datefmt: bool = False
    ):

        self.tree_log = tree_log
        self.posterior_log = posterior_log
        self.sample_every = sample_every
        self.chain_length = chain_length
        self.chain_type = chain_type
        self.chain_number = chain_number
        self.ambiguities = ambiguities
        self.datefmt = datefmt

        self.alignment: dict = self.read_fasta(fasta=alignment_file)
        self.dates: dict = self.read_dates(date_file=date_file)

        if reference_file is not None:
            self.reference: dict = self.read_fasta(fasta=reference_file)

    @staticmethod
    def load_template(name: str):
        template_loader = jinja2.FileSystemLoader(
            searchpath=f"{Path(__file__).parent / 'templates'}"
        )
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(name)
        return template

    def read_fasta(self, fasta: Path) -> dict:
        fasta = {
            name: seq.upper() for name, seq in
            Fasta(str(fasta), build_index=False)  # capital bases
        }
        for name, seq in fasta.items():
            bases = set(seq)
            for base in bases:
                if base not in ('A', 'C', 'T', 'G', 'N') and not self.ambiguities:
                    raise CritterError(f'Sequence for {name} contains base other than ACTGN: {bases}')
        return fasta

    def read_dates(self, date_file: Path):
        
        # Names always in column 1, dates always in column 2, no header
        with date_file.open("r") as date_file_input:
            dates = {
                line.strip().split()[0]: line.strip().split()[1] 
                for line in date_file_input
            }
        # Check that no name or date is missing
        for name, date in dates.items():
            if date in NULL or name in NULL:
                raise CritterError(f'Missing data not allowed in date file [{name}: {date}]')
        # Check that all sequences from alignment have a date
        for name in self.alignment.keys():
            if name not in dates.keys():
                raise CritterError(f'Aligned sequence {name} does not have a date')
        # If the date column is in date format DD/MM/YYYY
        if self.datefmt:
            dates = get_float_dates(dates)
        # Get only dates that are in sequence alignment
        seq_dates = {name: date for name, date in dates.items() if name in self.alignment.keys()}        
        return seq_dates

    # XML BLOCKS FOR BASE PARAMS

    @property
    def xml_run(self) -> str:
        if self.chain_type in ('coupled', 'adaptive', 'mcmcmc'):
            return f'<run ' \
                f'id="mcmc" ' \
                f'spec="beast.coupledMCMC.CoupledMCMC" ' \
                f'chainLength="{self.chain_length}" ' \
                f'chains="{self.chain_number}" ' \
                f'target="0.234" ' \
                f'logHeatedChains="false" ' \
                f'deltaTemperature="0.1" ' \
                f'optimise="true" ' \
                f'resampleEvery="{self.sample_every}">'
        else:
            return f'<run ' \
                f'id="mcmc" ' \
                f'spec="MCMC" ' \
                f'chainLength="{self.chain_length}">'

    @property
    def xml_dates(self) -> str:
        return ",".join([
            f'{name}={date}' for name, date in self.dates.items()
        ])

    @property
    def xml_alignment(self) -> str:
        data_block = ""
        for name, seq in self.alignment.items():
            data_block += f'<sequence ' \
                f'id="seq_{name}" ' \
                f'spec="Sequence" ' \
                f'taxon="{name}" ' \
                f'value="{seq}"/>\n'
        return data_block

    @property
    def xml_ambiguities(self) -> str:
        if self.ambiguities:
            return 'useAmbiguities="true"'
        else:
            return 'useAmbiguities="false"'
