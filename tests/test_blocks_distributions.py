from critter.blocks.parameters import RealParameter
from critter.blocks.distributions import Distribution
from critter.blocks.distributions import Uniform
from critter.blocks.distributions import Exponential
from critter.blocks.distributions import Gamma
from critter.blocks.distributions import Beta
from critter.blocks.distributions import LogNormal


def test_base_distribution_create_success():
    """
    GIVEN: Distribution with valid name or parameters
    WHEN:  Distribution instance is created
    THEN:  Distribution instance is created with valid defaults
    """
    no_param_distr = Distribution(
        id="Base"
    )
    assert no_param_distr.id == "Base"
    assert no_param_distr.params == list()
    assert type(no_param_distr.id) == str
    # Multiple param distribution
    param1 = RealParameter(
        id="test1",
        name="alpha",
        value=2.0
    )
    param2 = RealParameter(
        id="test2",
        name="beta",
        value=2.0
    )
    param_distr = Distribution(
        id="Base"
    )
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
    distr = Distribution(
        id="Base"
    )
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
    distr = Distribution(
        id="Base"
    )
    assert distr._get_distr_config() == ""


def test_base_distribution_default_xml_string():
    """
    GIVEN: Distribution with valid name
    WHEN:  Distribution instance calls __str__
    THEN:  Distribution instance returns valid XML string
    """
    xml = str(Distribution(
        id="Gamma"
    ))
    no_param_xml = f'<Distribution ' \
                   f'id="Gamma"  ' \
                   f'name="distr">' \
                   f'</Distribution>'  # space!
    assert xml == no_param_xml
    # Multiple parameter XML distribution string
    param1 = RealParameter(
        id='test1',
        name="alpha",
        value=2.0
    )
    param2 = RealParameter(
        id='test2',
        name="beta",
        value=2.0
    )
    xml = Distribution(
        id="Base"
    )
    xml.params = [param1, param2]
    param_xml = f'<Distribution ' \
                f'id="Base"  ' \
                f'name="distr">' \
                f'{str(param1)}' \
                f'{str(param2)}' \
                f'</Distribution>'  # space!
    assert str(xml) == param_xml


def test_distributions_create_id_success():
    """
    GIVEN: Distribution subclass with valid ID
    WHEN:  Distribution subclass instance is created
    THEN:  Distribution subclass instance is created with valid ID
    """
    uni = Uniform(
        id='test'
    )
    exp = Exponential(
        id='test',
        mean=1.0
    )
    beta = Beta(
        id='test',
        alpha=1.0,
        beta=0.5
    )
    gamma = Gamma(
        id='test',
        alpha=1.0,
        beta=0.5
    )
    lgn = LogNormal(
        id='test',
        mean=1.0,
        sd=2.0,
        real_space=True
    )

    assert str(uni).startswith('<Uniform id="test" ')
    assert str(exp).startswith('<Exponential id="test" ')
    assert str(beta).startswith('<Beta id="test" ')
    assert str(gamma).startswith('<Gamma id="test" ')
    assert str(lgn).startswith('<LogNormal id="test" ')


def test_distributions_create_param_success():
    """
    GIVEN: Distribution subclass with valid params for internal RealParameters
    WHEN:  Distribution subclass instance is created
    THEN:  Distribution subclass instance string contains the correct RealParameter string
    """
    # Uniform has no params, default param identifiers generated with UUID (e.g. exp.mean_id)
    exp = Exponential(
        id='test',
        mean=1.0
    )
    beta = Beta(
        id='test',
        alpha=1.0,
        beta=0.5
    )
    gamma = Gamma(
        id='test',
        alpha=1.0,
        beta=0.5
    )
    lgn = LogNormal(
        id='test',
        mean=1.0,
        sd=2.0,
        real_space=True
    )
    # RealParameter block strings using the random param identifiers from super class for validation
    mean_param_exp = str(
        RealParameter(
            name='mean',
            id=exp.mean_id,
            value=exp.mean
        )
    )
    alpha_param_beta = str(
        RealParameter(
            name='alpha',
            id=beta.alpha_id,
            value=beta.alpha
        )
    )
    alpha_param_gamma = str(
        RealParameter(
            name='alpha',
            id=gamma.alpha_id,
            value=gamma.alpha
        )
    )
    beta_param_beta = str(
        RealParameter(
            name='beta',
            id=beta.beta_id,
            value=beta.beta
        )
    )
    beta_param_gamma = str(
        RealParameter(
            name='beta',
            id=gamma.beta_id,
            value=gamma.beta
        )
    )
    mean_param_lgn = str(
        RealParameter(
            name='M',
            id=lgn.mean_id,
            value=lgn.mean
        )
    )
    sd_param_lgn = str(
        RealParameter(
            name='S',
            id=lgn.sd_id,
            value=lgn.sd
        )
    )

    assert mean_param_exp in str(exp)
    assert mean_param_lgn in str(lgn)
    assert sd_param_lgn in str(lgn)
    assert alpha_param_beta in str(beta)
    assert beta_param_beta in str(beta)
    assert alpha_param_gamma in str(gamma)
    assert beta_param_gamma in str(gamma)

