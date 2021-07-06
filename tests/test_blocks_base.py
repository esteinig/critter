import pytest

from pydantic import ValidationError
from critter.blocks.base import RealParameter, Distribution, Prior, infinity
from critter.blocks.distributions import Exponential
from critter.errors import CritterError

# Remember to check Pydantic --> usage/models/#data-conversion


def test_real_parameter_create_success():
    """
    GIVEN: RealParameter with valid name and value
    WHEN:  RealParameter instance is created
    THEN:  RealParameter instance is created with valid defaults
    """
    param = RealParameter(id="test", name="alpha", value=1.0)
    assert param.id == 'test'
    assert param.name == 'alpha'
    assert param.value == 1.0
    assert param.lower == -infinity
    assert param.upper == infinity
    assert param.dimension == 1
    assert param.estimate is False
    assert type(param.id) == str  # is uuid correctly returned as str


def test_real_parameter_create_failure():
    """
    GIVEN: RealParameter with invalid values
    WHEN:  RealParameter instance is created
    THEN:  RealParameter instances raises pydantic.ValidationError
    """

    # Required is null
    with pytest.raises(ValidationError):
        RealParameter(id=None, name="alpha", value=1.0)
    with pytest.raises(ValidationError):
        RealParameter(id='test', name=None, value=1.0)
    with pytest.raises(ValidationError):
        RealParameter(id='test', name="alpha", value=None)

    # Missing required
    with pytest.raises(ValidationError):
        RealParameter(name="alpha", value=1.0)
    with pytest.raises(ValidationError):
        RealParameter(id='test', value=1.0)
    with pytest.raises(ValidationError):
        RealParameter(id='test', name="alpha")

    # Defaults changed to null
    with pytest.raises(ValidationError):
        RealParameter(id='test', name="alpha", value=1.0, dimension=None)
    with pytest.raises(ValidationError):
        RealParameter(id='test', name="alpha", value=1.0, estimate=None)
    with pytest.raises(ValidationError):
        RealParameter(id='test', name="alpha", value=1.0, lower=None)
    with pytest.raises(ValidationError):
        RealParameter(id='test', name="alpha", value=1.0, upper=None)


def test_real_parameter_default_xml_string():
    """
    GIVEN: RealParameter with valid name and value
    WHEN:  RealParameter instance calls __str__
    THEN:  RealParameter instance returns valid XML string
    """
    xml = str(RealParameter(id='test', name="alpha", value=1.0))
    valid_xml = f'<parameter id="test" spec="parameter.RealParameter" estimate="false" ' \
        f'lower="-inf" upper="inf" name="alpha">1.0</parameter>'
    assert xml == valid_xml


def test_base_distribution_create_success():
    """
    GIVEN: Distribution with valid name or parameters
    WHEN:  Distribution instance is created
    THEN:  Distribution instance is created with valid defaults
    """
    no_param_distr = Distribution(id="Base")
    assert no_param_distr.id == "Base"
    assert no_param_distr.params == list()
    assert type(no_param_distr.id) == str

    param1 = RealParameter(id="test1", name="alpha", value=2.0)
    param2 = RealParameter(id="test2", name="beta", value=2.0)
    param_distr = Distribution(id="Base")
    param_distr.params = [param1, param2]
    assert param_distr.params == [param1, param2]
    assert type(param_distr.params[0]) == RealParameter
    assert type(param_distr.params[1]) == RealParameter


def test_base_distribution_attr_config_complete():
    """
    GIVEN:  Distribution with valid name
    WHEN:   Distribution instance has been created
    THEN:   Distribution instance config is complete
    """
    distr = Distribution(id="Base")
    for key, value in {'mode': 'mode', 'real_space': 'meanInRealSpace'}.items():
        assert key in distr._attr_name.keys()
        assert value in distr._attr_name.values()


def test_base_distribution_attr_config_string():
    """
    GIVEN:  Distribution with _attr_name config attribute
    WHEN:   Distribution instance calls _get_distr_config
    THEN:   Distribution instance returns empty config string
    """
    distr = Distribution(id="Base")
    assert distr._get_distr_config() == ""


def test_base_distribution_default_xml_string():
    """
    GIVEN: Distribution with valid name
    WHEN:  Distribution instance calls __str__
    THEN:  Distribution instance returns valid XML string
    """
    xml = str(Distribution(id="Gamma"))
    no_param_xml = f'<Distribution id="Gamma"  name="distr"></Distribution>'  # space!
    assert xml == no_param_xml

    param1 = RealParameter(id='test1', name="alpha", value=2.0)
    param2 = RealParameter(id='test2', name="beta", value=2.0)
    xml = Distribution(id="Base")
    xml.params = [param1, param2]
    param_xml = f'<Distribution id="Base"  name="distr">{str(param1)}{str(param2)}</Distribution>'  # space!
    assert str(xml) == param_xml


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

    intervals = " ".join(str(i) for i in prior.intervals)
    # Slices are only configured for birth-death model priors
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
    with pytest.raises(CritterError):
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
    with pytest.raises(CritterError):
        _ = prior.xml_slice_rate
