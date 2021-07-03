import pytest

from beastling.blocks.base import RealParameter, infinity
from pydantic import ValidationError


def test_real_parameter_create_default_success():
    """
    GIVEN: RealParameter with valid name and value
    WHEN:  RealParameter instance is created
    THEN:  RealParameter instance is created with valid defaults
    """
    param = RealParameter(name="alpha", value=1.0)
    assert param.name == 'alpha'
    assert param.value == 1.0
    assert param.lower == -infinity
    assert param.upper == infinity
    assert param.dimension == 1
    assert param.estimate is False
    assert type(param.id) == str  # is uuid correctly returned as str


def test_real_parameter_create_default_failure():
    """
    GIVEN: RealParameter with valid name and invalid value
    WHEN:  RealParameter instance is created
    THEN:  RealParameter instances raises pydantic.ValidationError
    """
    with pytest.raises(ValidationError):
        RealParameter(name="alpha", value=None)
        RealParameter(name=None, value=1.0)
        RealParameter(name="alpha", value=1.0, dimension=None)
        RealParameter(name="alpha", value=1.0, estimate=None)
        RealParameter(name="alpha", value=1.0, lower=None)
        RealParameter(name="alpha", value=1.0, upper=None)
        RealParameter(name="alpha", value=1.0, id=None)
