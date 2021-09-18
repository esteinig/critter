from pytest import fixture
from pathlib import Path
from critter.blocks.parameters import infinity
from critter.blocks.distributions import Beta
from critter.blocks.distributions import Gamma
from critter.blocks.distributions import LogNormal
from critter.blocks.distributions import Exponential
from critter.blocks.clocks import StrictClock
from critter.blocks.priors import OriginPrior
from critter.blocks.priors import ClockRatePrior
from critter.blocks.priors import ReproductiveNumberPrior
from critter.blocks.priors import SamplingProportionPrior
from critter.blocks.priors import BecomeUninfectiousRatePrior

@fixture
def critter_dates_ok() -> Path:
    return Path(__file__).parent / 'data' / 'test_dates_ok.tsv'


@fixture
def critter_dates_bad1() -> Path:
    return Path(__file__).parent / 'data' / 'test_dates_bad1.tsv'


@fixture
def critter_dates_bad2() -> Path:
    return Path(__file__).parent / 'data' / 'test_dates_bad2.tsv'


@fixture
def critter_alignment_ok() -> Path:
    return Path(__file__).parent / 'data' / 'test_alignment_ok.fasta'


@fixture
def critter_alignment_bad() -> Path:
    return Path(__file__).parent / 'data' / 'test_alignment_bad.fasta'


@fixture
def critter_reference_ok() -> Path:
    return Path(__file__).parent / 'data' / 'test_reference_ok.fasta'


@fixture
def critter_alignment_xml() -> str:
    return '<sequence id="seq_seq1" spec="Sequence" taxon="seq1" totalcount="4" value="ACTG"/>\n' \
        '<sequence id="seq_seq2" spec="Sequence" taxon="seq2" totalcount="4" value="ACTG"/>\n' \
        '<sequence id="seq_seq3" spec="Sequence" taxon="seq3" totalcount="4" value="ACTG"/>\n'


@fixture
def critter_date_xml() -> str:
    return "seq1=2015.12,seq2=2016.12,seq3=2017.12"


@fixture
def critter_run_xml_mcmc() -> str:
    return '<run id="mcmc" spec="MCMC" chainLength="100000">'


@fixture
def critter_run_xml_mcmcmc() -> str:
    return '<run id="mcmc" spec="beast.coupledMCMC.CoupledMCMC" chainLength="100000" chains="4" target="0.234" ' \
        'logHeatedChains="false" deltaTemperature="0.1" optimise="true" resampleEvery="1000">'


@fixture
def bdss_sampling_proportion_slice_function_xml() -> str:
    return '<function spec="beast.core.util.Slice" id="samplingProportion1" arg="@samplingProportion" index="0" count="1"/>\n' \
        '<function spec="beast.core.util.Slice" id="samplingProportion2" arg="@samplingProportion" index="1" count="1"/>\n'


@fixture
def bdss_sampling_proportion_slice_logger_xml() -> str:
    return '<log idref="samplingProportion1"/>\n' \
        '<log idref="samplingProportion2"/>\n'


@fixture 
def bdss_sampling_proportion_slice_rate_change_times_xml() -> str:
    return '<samplingRateChangeTimes spec="beast.core.parameter.RealParameter" value="13.1 0.0"/>\n' \
        '<reverseTimeArrays spec="beast.core.parameter.BooleanParameter" value="false false true false false"/>\n'

@fixture
def bdss_strict_clock_model() -> StrictClock:
    return StrictClock(
        prior=[
            ClockRatePrior(
                distribution=[
                    LogNormal(mean=0.0004, sd=0.3)
                ],
                initial=[0.0005],
                lower=0,
                upper=infinity,
                dimension=1
            )
        ]
    )


@fixture
def bdss_origin_prior() -> OriginPrior:
    return OriginPrior(
        distribution=[
            Gamma(alpha=2.0, beta=40.0)
        ],
        initial=[60.0],
        lower=0,
        upper=infinity,
        dimension=1
    )

@fixture
def bdss_sampling_proportion_prior() -> SamplingProportionPrior:
    return SamplingProportionPrior(
        distribution=[
            Beta(alpha=1.0, beta=1.0)
        ],
        initial=[0.01],
        lower=0,
        upper=1.0,
        dimension=1,
        sliced=False
    )


@fixture
def bdss_sampling_proportion_prior_sliced() -> SamplingProportionPrior:
    return SamplingProportionPrior(
        distribution=[
            Exponential(mean=1e-08),  # fixed to 0
            Beta(alpha=1.0, beta=1.0)
        ],
        initial=[0, 0.01], # fixed to 0
        lower=0,
        upper=1.0,
        dimension=2,
        sliced=True,
        intervals=[13.1, 0.0]
    )


@fixture
def bdss_reproductive_number_prior() -> ReproductiveNumberPrior:
    return ReproductiveNumberPrior(
        distribution=[
            Gamma(alpha=2.0, beta=2.0)
        ],
        initial=[2.0],
        lower=0,
        upper=infinity,
        dimension=5
    )


@fixture
def bdss_become_uninfectious_rate_prior() -> BecomeUninfectiousRatePrior:
    return BecomeUninfectiousRatePrior(
        distribution=[
            LogNormal(mean=1.0, sd=1.0)
        ],
        initial=[1.0],
        lower=0,
        upper=infinity,
        dimension=1
    )