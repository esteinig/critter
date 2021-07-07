from critter.blocks.clocks import Clock
from critter.blocks.priors import Rate
from critter.blocks.priors import Prior
from critter.blocks.priors import UCLDSD
from critter.blocks.priors import UCLDMean


def test_clock_base_create_success():
    """
    GIVEN: Clock model with valid parameters
    WHEN:  Clock instance is created
    THEN:  Clock instance is created with valid default parameters
    """

    prior = Rate()  # standard rate prior for strict clock
    clock = Clock(priors=[prior], fixed=False, state_node='')
    assert clock.id.startswith("Clock.")
    assert clock.fixed is False
    assert clock.state_node == ''
    assert isinstance(clock.priors[0], Prior)

    # Returns valid XMLs for single prior config of clock model
    assert clock.xml_state_node == clock.state_node
    assert clock.xml == prior.xml
    assert clock.xml_prior == prior.xml
    assert clock.xml_param == prior.xml_param
    assert clock.xml_logger == prior.xml_logger

    # Clock subclass XMLs not defined in base class
    assert clock.xml_scale_operator == ''
    assert clock.xml_updown_operator == ''
    assert clock.xml_branch_rate_model == ''

    # Clock base with multiple priors
    ucld_mean, ucld_sd = UCLDMean(), UCLDSD()
    clock = Clock(priors=[ucld_mean, ucld_sd], fixed=False, state_node='')
