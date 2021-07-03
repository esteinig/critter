import pytest

from pydantic import ValidationError
from beastling.blocks.base import RealParameter, Distribution, infinity

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

    with pytest.raises(ValidationError):
        RealParameter(id=None, name="alpha", value=1.0)
        RealParameter(id='test', name=None, value=1.0)
        RealParameter(id='test', name="alpha", value=None)
        RealParameter(id='test', name="alpha", value=1.0, dimension=None)
        RealParameter(id='test', name="alpha", value=1.0, estimate=None)
        RealParameter(id='test', name="alpha", value=1.0, lower=None)
        RealParameter(id='test', name="alpha", value=1.0, upper=None)



def test_real_parameter_xml_string():
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
    no_param_distr = Distribution(id="Gamma")
    assert no_param_distr.id == "Gamma"
    assert no_param_distr.params == list()
    assert type(no_param_distr.id) == str

    param1 = RealParameter(id="test1", name="alpha", value=2.0)
    param2 = RealParameter(id="test2", name="beta", value=2.0)
    param_distr = Distribution(id="Gamma", params=[param1, param2])
    assert param_distr.params == [param1, param2]
    assert type(param_distr.params[0]) == RealParameter
    assert type(param_distr.params[1]) == RealParameter


def test_base_distribution_attr_config_complete():
    """
    GIVEN:  Distribution with valid name
    WHEN:   Distribution instance has been created
    THEN:   Distribution instance config is complete
    """
    distr = Distribution(id="Gamma")
    for key, value in {'mode': 'mode', 'real_space': 'meanInRealSpace'}.items():
        assert key in distr._attr_name.keys()
        assert value in distr._attr_name.values()


def test_base_distribution_attr_config_string():
    """
    GIVEN:  Distribution with _attr_name config attribute
    WHEN:   Distribution instance calls _get_distr_config
    THEN:   Distribution instance returns empty config string
    """
    distr = Distribution(id="Gamma")
    assert distr._get_distr_config() == ""


def test_base_distribution_xml_string():
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
    xml = str(Distribution(id="Gamma", params=[param1, param2]))
    param_xml = f'<Distribution id="Gamma"  name="distr">{str(param1)}{str(param2)}</Distribution>'  # space!
    assert xml == param_xml

