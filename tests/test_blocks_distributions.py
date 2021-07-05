import pytest

from pydantic import ValidationError
from critter.blocks.distributions import RealParameter
from critter.blocks.distributions import Uniform
from critter.blocks.distributions import Exponential
from critter.blocks.distributions import Gamma
from critter.blocks.distributions import Beta
from critter.blocks.distributions import LogNormal


def test_distributions_create_id_success():
    """
    GIVEN: Distribution subclass with valid ID
    WHEN:  Distribution subclass instance is created
    THEN:  Distribution subclass instance is created with valid ID
    """
    uni = Uniform(id='test')
    exp = Exponential(id='test', mean=1.0)
    beta = Beta(id='test', alpha=1.0, beta=0.5)
    gamma = Gamma(id='test', alpha=1.0, beta=0.5)
    lgn = LogNormal(id='test', mean=1.0, sd=2.0, real_space=True)

    assert str(uni).startswith('<Uniform id="test" ')
    assert str(exp).startswith('<Exponential id="test" ')
    assert str(beta).startswith('<Beta id="test" ')
    assert str(gamma).startswith('<Gamma id="test" ')
    assert str(lgn).startswith('<LogNormal id="test" ')


def test_distributions_create_param_failure():
    """
    GIVEN: Distribution subclass with invalid parameters
    WHEN:  Distribution subclass instance is created
    THEN:  Distribution subclass instance raises
                TypeError for missing params
                pydantic.ValidationError for null values
    """

    # Missing required params
    with pytest.raises(TypeError):
        Exponential(id='test')
    with pytest.raises(TypeError):
        Beta(id='test')
    with pytest.raises(TypeError):
        Gamma(id='test')
    with pytest.raises(TypeError):
        LogNormal(id='test')

    # Params are passed null values
    with pytest.raises(ValidationError):
        Exponential(id='test', mean=None)
    with pytest.raises(ValidationError):
        Beta(id='test', alpha=None, beta=None)
    with pytest.raises(ValidationError):
        Gamma(id='test', alpha=None, beta=None)
    with pytest.raises(ValidationError):
        LogNormal(id='test', mean=None, sd=None)


def test_distributions_create_param_success():
    """
    GIVEN: Distribution subclass with valid params for internal RealParameters
    WHEN:  Distribution subclass instance is created
    THEN:  Distribution subclass instance string contains the correct RealParameter string
    """
    # Uniform has no params, default param identifiers generated with UUID (e.g. exp.mean_id)
    exp = Exponential(id='test', mean=1.0)
    beta = Beta(id='test', alpha=1.0, beta=0.5)
    gamma = Gamma(id='test', alpha=1.0, beta=0.5)
    lgn = LogNormal(id='test', mean=1.0, sd=2.0, real_space=True)

    # RealParameter block strings using the random param identifiers from super class for validation
    mean_param_exp = str(RealParameter(name='mean', id=exp.mean_id, value=exp.mean))
    alpha_param_beta = str(RealParameter(name='alpha', id=beta.alpha_id, value=beta.alpha))
    alpha_param_gamma = str(RealParameter(name='alpha', id=gamma.alpha_id, value=gamma.alpha))
    beta_param_beta = str(RealParameter(name='beta', id=beta.beta_id, value=beta.beta))
    beta_param_gamma = str(RealParameter(name='beta', id=gamma.beta_id, value=gamma.beta))
    mean_param_lgn = str(RealParameter(name='mean', id=lgn.mean_id, value=lgn.mean))
    sd_param_lgn = str(RealParameter(name='sd', id=lgn.sd_id, value=lgn.sd))

    assert mean_param_exp in str(exp)
    assert mean_param_lgn in str(lgn)
    assert sd_param_lgn in str(lgn)
    assert alpha_param_beta in str(beta)
    assert beta_param_beta in str(beta)
    assert alpha_param_gamma in str(gamma)
    assert beta_param_gamma in str(gamma)

