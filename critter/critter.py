import pandas
import jinja2
from pathlib import Path
from pyfastx import Fasta
from critter.errors import CritterError


class Critter:

    def __init__(
        self,
        reference_file: Path,
        alignment_file: Path,
        date_file: Path,
        tree_log: Path = Path('trees.log'),
        posterior_log: Path = Path('posteriors.log'),
        sample_every: int = 1000,
        chain_length: int = 100000,
        chain_type: str = 'default',
        chain_number: int = 4,
        output_prefix: str = "bdss",
        missing_dates: bool = False
    ):

        self.xml = None  # rendered template

        self.reference: dict = self.read_fasta(fasta=reference_file)
        self.alignment: dict = self.read_fasta(fasta=alignment_file)
        self.dates: pandas.DataFrame = self.read_dates(date_file=date_file)

        self.tree_log = tree_log
        self.posterior_log = posterior_log

        self.sample_every = sample_every
        self.chain_length = chain_length
        self.chain_type = chain_type
        self.chain_number = chain_number
        self.output_prefix = output_prefix
        self.missing_dates = missing_dates

    @staticmethod
    def load_template(name: str):
        """ Load template file for a model """
        template_loader = jinja2.FileSystemLoader(
            searchpath=f"{Path(__file__).parent / 'templates'}"
        )
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(name)
        return template

    @staticmethod
    def read_fasta(fasta: Path) -> dict:
        return {
            name: seq.upper() for name, seq in
            Fasta(str(fasta), build_index=False)  # capital bases
        }

    def read_dates(self, date_file: Path):
        df = pandas.read_csv(date_file, sep='\t', header=None, na_values=['-'], names=['name', 'date'])
        if not self.missing_dates:
            if '-' in df['date'].tolist():
                raise CritterError('Dates for all sequences must be specified')
        return df

    def check_dates(self):

        for name in self.alignment.keys():
            if name not in self.dates['name']:
                raise CritterError(f'Aligned sequence {name} does not have a date')
        self.dates = self.dates[self.dates['name'].isin(self.alignment.keys())]

    # XML BLOCKS FOR BASE PARAMS

    @property
    def xml_run(self) -> str:
        if self.chain_type == 'coupled':
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
            f'{row["name"]}={row["date"]}' for i, row in self.dates.iterrows()
        ])

    @property
    def xml_alignment(self) -> str:
        data_block = ""
        for name, seq in self.alignment.items():
            bases = set(seq)
            for base in bases:
                if base not in ('A', 'C', 'T', 'G', 'N'):
                    raise CritterError(f'Sequence for {name} contains base other than ACTGN: {bases}')
            data_block += f'<sequence ' \
                f'id="seq_{name}" ' \
                f'spec="Sequence" ' \
                f'taxon="{name}" ' \
                f'totalcount="{len(bases)}" ' \
                f'value="{seq}"/>\n'
        return data_block
