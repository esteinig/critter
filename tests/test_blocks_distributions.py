import pytest

from pydantic import ValidationError
from critter.blocks.distributions import RealParameter
from critter.blocks.distributions import Distribution
from critter.blocks.distributions import Uniform
from critter.blocks.distributions import Exponential
from critter.blocks.distributions import Gamma
from critter.blocks.distributions import Beta
from critter.blocks.distributions import LogNormal


def test_distributions_create_success():
    """
    GIVEN: Distribution subclass with valid parameters
    WHEN:  Distribution subclass instance is created
    THEN:  Distribution subclass instance is created with valid defaults
    """
    uniform = Uniform(id='test')
    exponential = Exponential(id='test', mean=0.5)
    beta = Beta(id='test', alpha=1.0, beta=0.5)
    gamma = Gamma(id='test', alpha=1.0, beta=0.5)
    lognormal = LogNormal(id='test', mean=1.0, sd=0.5)

    assert str(uniform).startswith('<Uniform id="test" ')
    assert str(exponential).startswith('<Exponential id="test" ')
    assert str(beta).startswith('<Beta id="test" ')
    assert str(gamma).startswith('<Gamma id="test" ')
    assert str(lognormal).startswith('<LogNormal id="test" ')
