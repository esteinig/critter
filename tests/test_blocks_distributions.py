from critter.blocks.parameters import RealParameter
from critter.blocks.distributions import Distribution
from critter.blocks.distributions import Uniform
from critter.blocks.distributions import Exponential
from critter.blocks.distributions import Gamma
from critter.blocks.distributions import Beta
from critter.blocks.distributions import LogNormal


def test_distribution_create_unique_success():
    """
    GIVEN: Distribution instance with deafult parameters
    WHEN:  Distribution instance is created
    THEN:  Distribution instance is created with unique identifiers
    """
    distr1, distr2 = Distribution(), Distribution()

    uni1, uni2 = Uniform(), Uniform()
    exp1, exp2 = Exponential(
        mean=1.0
    ), Exponential(
        mean=1.0
    )
    gam1, gam2 = Gamma(
        alpha=1.0,
        beta=1.0
    ), Gamma(
        alpha=1.0,
        beta=1.0
    )
    bet1, bet2 = Beta(
        alpha=1.0, 
        beta=1.0
    ), Beta(
        alpha=1.0, 
        beta=1.0
    )
    lgn1, lgn2 = LogNormal(
        mean=1.0, 
        sd=1.0
    ), LogNormal(
        mean=1.0, 
        sd=1.0
    )

    assert distr1._id != distr2._id
    assert uni1._id != uni2._id
    assert exp1._id != exp2._id
    assert gam1._id != gam2._id
    assert bet1._id != bet2._id
    assert lgn1._id != lgn2._id

def test_base_distribution_attr_config_complete():
    """
    GIVEN:  Distribution with valid name
    WHEN:   Distribution instance has been created
    THEN:   Distribution instance config is complete
    """
    distr = Distribution()
    for key, value in {
        'mode': 'mode',
        'real_space': 'meanInRealSpace',
        'sd_parameter': 'S'
    }.items():
        assert key in distr._attr_name.keys()
        assert value in distr._attr_name.values()


def test_base_distribution_attr_config_string():
    """
    GIVEN:  Distribution with _attr_name config attribute
    WHEN:   Distribution instance calls _get_distr_config
    THEN:   Distribution instance returns empty config string
    """
    distr = Distribution()
    assert distr._get_distr_config() == ""


def test_distributions_create_param_success():
    """
    GIVEN: Distribution subclass with valid params for internal RealParameters
    WHEN:  Distribution subclass instance is created
    THEN:  Distribution subclass instance string contains the correct RealParameter string
    """

    uni = Uniform()

    exp = Exponential(
        mean=1.0
    )
    beta = Beta(
        alpha=1.0,
        beta=0.5
    )
    gamma = Gamma(
        alpha=1.0,
        beta=0.5
    )
    lgn = LogNormal(
        mean=1.0,
        sd=2.0,
        real_space=True
    )
    mean_param_exp = str(
        RealParameter(
            name='mean',
            id=exp._mean_id,
            value=exp.mean,
            estimate=False  # Distribution parameters are not estimated
        )
    )
    alpha_param_beta = str(
        RealParameter(
            name='alpha',
            id=beta._alpha_id,
            value=beta.alpha,
            estimate=False
        )
    )
    alpha_param_gamma = str(
        RealParameter(
            name='alpha',
            id=gamma._alpha_id,
            value=gamma.alpha,
            estimate=False
        )
    )
    beta_param_beta = str(
        RealParameter(
            name='beta',
            id=beta._beta_id,
            value=beta.beta,
            estimate=False
        )
    )
    beta_param_gamma = str(
        RealParameter(
            name='beta',
            id=gamma._beta_id,
            value=gamma.beta,
            estimate=False
        )
    )
    mean_param_lgn = str(
        RealParameter(
            name='M',
            id=lgn._mean_id,
            value=lgn.mean,
            estimate=False
        )
    )
    sd_param_lgn = str(
        RealParameter(
            name='S',
            id=lgn._sd_id,
            value=lgn.sd,
            estimate=False
        )
    )

    assert uni._params == []
    assert mean_param_exp in str(exp)
    assert mean_param_lgn in str(lgn)
    assert sd_param_lgn in str(lgn)
    assert alpha_param_beta in str(beta)
    assert beta_param_beta in str(beta)
    assert alpha_param_gamma in str(gamma)
    assert beta_param_gamma in str(gamma)

def test_distributions_lognormal_none_success():
    """
    GIVEN: LogNormal sistribution with no params for internal RealParameters
    WHEN:  Distribution subclass instance is created
    THEN:  Distribution subclass instance string contains the correct RealParameter string
    """

    # Special case for the UCRLBranchRateModel parameterisation 
    # which for some arcane reason contains the SD parameter
    # inside the distribution main parameter definitions (HTML)
    
    lgn1 = LogNormal(
        mean=None,
        sd=2.0
    )
    lgn2 = LogNormal(
        mean=1.0,
        sd=None
    )
    lgn3 = LogNormal(
        mean=None,
        sd=None
    )

    assert len(lgn1._params) == 1
    assert len(lgn2._params) == 1
    assert len(lgn3._params) == 0