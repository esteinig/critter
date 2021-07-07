from pytest import raises
from math import inf as infinity
from pydantic import ValidationError
from critter.blocks.priors import Prior
from critter.blocks.priors import Origin
from critter.blocks.priors import Rho
from critter.blocks.priors import SamplingProportion
from critter.blocks.priors import ReproductiveNumber
from critter.blocks.priors import BecomeUninfectiousRate
from critter.blocks.priors import RateMatrix
from critter.blocks.priors import PopulationSize
from critter.blocks.priors import GroupSize
from critter.blocks.priors import SamplingProportionMTBD
from critter.blocks.distributions import Distribution
from critter.blocks.distributions import Exponential
from critter.blocks.parameters import RealParameter


def test_prior_create_default_success():
    """
    GIVEN: Prior with valid params for a non-sliced configuration
    WHEN:  Prior instance is created
    THEN:  Prior instance is created with valid defaults
    """
    prior = Prior(
        id="samplingProportion", distribution=[Exponential(mean=0.5)], initial=[1.0], dimension=1
    )
    # Default attributes
    assert prior.initial == [1.0]
    assert isinstance(prior.distribution[0], Distribution)
    assert prior.id == "samplingProportion"
    assert prior.dimension == 1
    assert prior.lower == -infinity
    assert prior.upper == infinity
    assert prior.sliced is False
    assert prior.intervals == list()
    assert prior.scw is None
    assert prior.scx is None
    assert prior.param_spec == "parameter.RealParameter"
    # XML blocks
    assert prior.xml.startswith(f'<prior id="{prior.id}Prior" name="distribution" x="@{prior.id}">')
    assert prior.xml.endswith('</prior>')
    assert prior.distribution[0].xml in prior.xml
    # Test alias of xml property
    assert prior.xml_prior.startswith(f'<prior id="{prior.id}Prior" name="distribution" x="@{prior.id}">')
    assert prior.xml_prior.endswith('</prior>')  # allow for line breaks at ends
    assert prior.distribution[0].xml in prior.xml_prior
    # Test of other xml properties
    assert prior.xml_scale_operator is None
    assert prior.xml_logger == f'<log idref="{prior.id}"/>'
    assert prior.xml_param == str(RealParameter(
            id=f"{prior.id}", name="stateNode",
            value=" ".join(str(i) for i in prior.initial) if len(prior.initial) > 1 else prior.initial[0],
            spec=prior.param_spec, dimension=prior.dimension, lower=prior.lower, upper=prior.upper
        ))
    assert prior.xml_slice_function == ''
    assert prior.xml_slice_rate == ''
    assert prior.xml_slice_logger == ''


# TODO: implement validators that constrain the prior slice config lists
def test_prior_create_sliced_success():
    """
    GIVEN: Prior with valid required params for a slice configuration
    WHEN:  Prior instance is created
    THEN:  Prior instance is created with valid defaults

    NOTE:  Sliced priors are only available usually for subclasses representing
           priors in the birth-death skyline models (origin, rho, sampling proportion,
           become uninfectious rate, and reproductive number) which are constrained
           in camel-case as >> slice_id << These are tested in the failure raising
           pydantic.ValidationError from validators
    """
    prior = Prior(
        id="samplingProportion",
        sliced=True,
        dimension=2,
        intervals=[10.1, 5.1],
        distribution=[Exponential(mean=0.5), Exponential(mean=1.0)],
        initial=[1.0, 2.0]
    )
    # Prior sliced configuration
    assert prior.initial == [1.0, 2.0]
    for inst in prior.distribution:
        assert isinstance(inst, Distribution)
        assert inst.xml in prior.xml
        assert inst.xml in prior.xml_prior
    assert prior.id == "samplingProportion"
    assert prior.dimension == 2
    assert prior.sliced is True
    assert prior.intervals == [10.1, 5.1]

    # Multiple priors for slices, get slice XMLs
    for i, distribution in enumerate(prior.distribution):
        true_prior_xml = f'<prior id="{prior.id}Slice{i+1}" name="distribution" ' \
                     f'x="@{prior.id}{i+1}">{distribution.xml}</prior>'
        assert true_prior_xml in prior.xml
        assert true_prior_xml in prior.xml_prior
        true_slice_func_xml = f'<function spec="beast.core.util.Slice" id="{prior.id}{i+1}" ' \
            f'arg="@{prior.id}" index="{i}" count="1"/>'
        assert true_slice_func_xml in prior.xml_slice_function
        true_slice_logger_xml = f'<log idref="{prior.id}{i+1}"/>'
        assert true_slice_logger_xml in prior.xml_slice_logger

    # Slices are only configured for birth-death model priors
    intervals = " ".join(str(i) for i in prior.intervals)
    for bd_prior, xml_spec in {
        "samplingProportion": "samplingRateChangeTimes",
        "rho": "samplingRateChangeTimes",
        "reproductiveNumber": "birthRateChangeTimes",
        "becomeUninfectious": "deathRateChangeTimes"
    }.items():
        prior.id = bd_prior
        true_slice_rate_xml = f'<{xml_spec} spec="beast.core.parameter.RealParameter" value="{intervals}"/>'
        assert true_slice_rate_xml in prior.xml_slice_rate


def test_prior_create_sliced_fail():
    """
    GIVEN: Prior with invalid id for a sliced configuration
    WHEN:  Prior instance fails to be created
    THEN:  CritterError is raised from Prior instance validator
    """
    with raises(ValidationError):
        Prior(
            id="nameFailsToInitSlicedPrior",  # slices only available for BD models
            sliced=True,  # ... when sliced is True
            dimension=2,
            intervals=[10.1, 5.1],
            distribution=[Exponential(mean=0.5), Exponential(mean=1.0)],
            initial=[1.0, 2.0]
        )


def test_prior_slice_rate_xml_fail():
    """
    GIVEN: Prior with invalid ID that evaded pydantic ValidationError
    WHEN:  Prior instance XML for a slice rate is accessed
    THEN:  CritterError is raised, as only defined for
    """
    prior = Prior(
        id="samplingProportion",
        sliced=True,
        dimension=2,
        intervals=[10.1, 5.1],
        distribution=[Exponential(mean=0.5), Exponential(mean=1.0)],
        initial=[1.0, 2.0]
    )  # success

    prior.id = "nameFailsToGetSliceRateXML"
    with raises(ValidationError):
        _ = prior.xml_slice_rate


def test_prior_subclass_create_success():
    """
    GIVEN: Prior subclassess with predefined identifiers and valid defaults
    WHEN:  Prior subclasses are created
    THEN:  Prior subclassses are created with valid default identifiers
    """
    distr, i = [Exponential(mean=0.5)], [1.0]
    assert Origin(distribution=distr, initial=i).id == 'origin'
    assert ReproductiveNumber(distribution=distr, initial=i).id == "reproductiveNumber"
    assert SamplingProportion(distribution=distr, initial=i).id == "samplingProportion"
    assert Rho(distribution=distr, initial=i).id == "rho"
    assert BecomeUninfectiousRate(distribution=distr, initial=i).id == "becomeUninfectiousRate"
    assert RateMatrix(distribution=distr, initial=i).id == "rateMatrix"
    assert PopulationSize(distribution=distr, initial=i).id == "bPopSizes"

    # Test modified XML properties of these two subclasses:
    sp_mtbd = SamplingProportionMTBD(distribution=distr, initial=i)
    ps_coal = GroupSize(distribution=distr, initial=i)
    assert sp_mtbd.id == "samplingProportion"
    assert ps_coal.id == "bGroupSizes"
    assert ps_coal.param_spec == "parameter.IntegerParameter"
    assert ps_coal.state_node_group_size == f'<stateNode id="bGroupSizes" spec="parameter.IntegerParameter" ' \
        f'dimension="{ps_coal.dimension}">{ps_coal.initial}</stateNode>'
    assert sp_mtbd.get_include_string() == (1, 'true')

    # Multi type birth death XML components
    _incl = sp_mtbd.get_include_string()
    _dist = f'<distribution id="{sp_mtbd.id}Prior"' \
            f' spec="multitypetree.distributions.ExcludablePrior"' \
            f' x="@{sp_mtbd.id}">'
    _xinclude = f'<xInclude id="samplingProportionXInclude" ' \
                f'spec="parameter.BooleanParameter" ' \
                f'dimension="{sp_mtbd.dimension}">{_incl}</xInclude>'
    assert sp_mtbd.xml.startswith(_dist)
    assert _xinclude in sp_mtbd.xml
    assert sp_mtbd.distribution[0].xml in sp_mtbd.xml
    assert sp_mtbd.xml.endswith('</distribution>')
