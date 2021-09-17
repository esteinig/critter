import pytest
from pydantic import ValidationError
from critter.blocks.branches import StrictBranchRateModel, UCREBranchRateModel, UCRLBranchRateModel
from critter.blocks.operators import ScaleOperator, UpDownOperator, SwapOperator, IntegerRandomWalkOperator, UniformOperator
from critter.blocks.clocks import Clock, StrictClock, UCREClock, UCRLClock
from critter.blocks.priors import Prior, ClockRatePrior, UCRLSDPrior, UCRLMeanPrior, UCREPrior, ReproductiveNumberPrior
from critter.blocks.distributions import Exponential


def test_clock_base_create_success():
    """
    GIVEN: Clock model with valid parameters
    WHEN:  Clock instance is created
    THEN:  Clock instance is created with valid default parameters
    """
    distr, i = [Exponential(mean=0.5)], [1.0]
    prior = ClockRatePrior(
        distribution=distr,
        initial=i
    )  # standard rate prior for strict clock
    clock = Clock(
        prior=[prior],
        fixed=False,
        state_node=''
    )
    assert clock.id.startswith("Clock.")
    assert clock.fixed is False
    assert clock.xml_state_node == ''
    assert isinstance(clock.prior[0], Prior)
    # Returns valid XMLs for single prior config of clock model
    assert clock.xml == prior.xml
    assert str(clock) == prior.xml
    assert clock.xml_prior == prior.xml
    assert clock.xml_param == prior.xml_param
    assert clock.xml_logger == prior.xml_logger
    # Clock subclass XMLs not defined in base class
    assert clock.xml_scale_operator == ''
    assert clock.xml_updown_operator == ''
    assert clock.xml_branch_rate_model == ''
    # Clock base with multiple priors
    ucld_mean = UCRLMeanPrior(
        distribution=distr,
        initial=i
    )
    ucld_sd = UCRLSDPrior(
        distribution=distr,
        initial=i
    )
    clock = Clock(
        prior=[ucld_mean, ucld_sd],
        fixed=False,
        state_node=''
    )
    assert clock.xml == "\n".join([ucld_mean.xml, ucld_sd.xml])


def test_clock_base_create_wrong_prior_failure():
    """
    GIVEN: Clock model with incorrect prior
    WHEN:  Clock instance is created
    THEN:  Clock instance fails with ValidationError
    """
    distr, i = [Exponential(mean=0.5)], [1.0]
    with pytest.raises(ValidationError):
        prior = ReproductiveNumberPrior(
            distribution=distr,
            initial=i
        )  # wrong rate prior for clocks
        Clock(
            prior=[prior],
            fixed=False,
            state_node=''
        )


def test_clock_strict_create_success():
    """
    GIVEN: StrictClock model with valid parameters
    WHEN:  StrictClock instance is created
    THEN:  StrictClock instance is created with valid parameters
    """
    distr, i = [Exponential(mean=0.5)], [1.0]
    strict_prior = ClockRatePrior(
        distribution=distr,
        initial=i
    )
    strict_clock = StrictClock(
        prior=[strict_prior]
    )
    assert strict_clock.xml_state_node == ''
    assert strict_clock.xml_branch_rate_model == StrictBranchRateModel(
        id="strictClockBranchRate",
        parameter="@clockRate"
    ).xml
    assert strict_clock.xml_scale_operator == ScaleOperator(
        id="strictClockScaleOperator",
        parameter="@clockRate"
    ).xml
    assert strict_clock.xml_updown_operator == UpDownOperator(
        id="strictClockUpDownOperator",
        parameter="@clockRate",
        up_parameter="@clockRate",
        down_parameter="@Tree"
    ).xml
    # Strict clock fixed
    strict_clock_fixed = StrictClock(
        prior=[strict_prior],
        fixed=True
    )
    assert strict_clock_fixed.xml_scale_operator == ''
    assert strict_clock_fixed.xml_updown_operator == ''


def test_clock_ucre_create_success():
    """
    GIVEN: UCREClock model with valid parameters
    WHEN:  UCREClock instance is created
    THEN:  UCREClock instance is created with valid parameters
    """

    distr, i = [Exponential(mean=0.5)], [1.0]
    ucre_prior = UCREPrior(
        distribution=distr,
        initial=i
    )
    ucre_clock = UCREClock(
        prior=[ucre_prior]
    )
    assert ucre_clock.xml_state_node == \
        f'<stateNode ' \
        f'id="ucreRateCategories" ' \
        f'spec="parameter.IntegerParameter" ' \
        f'dimension="718">' \
        f'1' \
        f'</stateNode>'
    assert ucre_clock.xml_branch_rate_model == UCREBranchRateModel(
        id="ucreBranchRateModel",
        parameter="@ucreMean",
        tree_parameter="@Tree",
        rate_categories_parameter="@ucreRateCategories"
    ).xml
    assert ucre_clock.xml_scale_operator == "\n".join([
        ScaleOperator(
            id="ucreMeanScaleOperator",
            parameter="@ucreMean",
        ).xml,
        IntegerRandomWalkOperator(
            id="ucreCategoriesRandomWalk",
            parameter="@ucreRateCategories"
        ).xml,
        SwapOperator(
            id="ucreCategoriesSwap",
            parameter="@ucreRateCategories"
        ).xml,
        UniformOperator(
            id="ucreCategoriesUniform",
            parameter="@ucreRateCategories"
        ).xml

    ])
    assert ucre_clock.xml_updown_operator == UpDownOperator(
        id="ucreMeanUpDownOperator",
        up_parameter="@ucreMean",
        down_parameter="@Tree"
    ).xml

    ucre_clock_fixed = UCREClock(
        prior=[ucre_prior],
        fixed=True
    )
    assert ucre_clock_fixed.xml_scale_operator == ''
    assert ucre_clock_fixed.xml_updown_operator == ''


def test_clock_ucrl_create_success():
    """
    GIVEN: UCRLClock model with valid parameters
    WHEN:  UCRLClock instance is created
    THEN:  UCRLClock instance is created with valid parameters
    """

    distr, i = [Exponential(mean=0.5)], [1.0]
    ucrl_mean_prior = UCRLMeanPrior(
        distribution=distr,
        initial=i
    )
    ucrl_sd_prior = UCRLSDPrior(
        distribution=distr,
        initial=i
    )
    ucrl_clock = UCRLClock(
        prior=[ucrl_mean_prior, ucrl_sd_prior]
    )
    assert ucrl_clock.xml_state_node == \
        f'<stateNode ' \
        f'id="ucrlRateCategories" ' \
        f'spec="parameter.IntegerParameter" ' \
        f'dimension="718">' \
        f'1' \
        f'</stateNode>'
    assert ucrl_clock.xml_branch_rate_model == UCRLBranchRateModel(
        id="ucrlBranchRateModel",
        parameter="@ucrlMean",
        tree_parameter="@Tree",
        rate_categories_parameter="@ucrlRateCategories"
    ).xml
    assert ucrl_clock.xml_scale_operator == "\n".join([
        ScaleOperator(
            id="ucrlMeanScaleOperator",
            parameter="@ucrlMean",
        ).xml,
        ScaleOperator(
            id="ucrlSDScaleOperator",
            parameter="@ucrlSD",
            weight=3.0
        ).xml,
        IntegerRandomWalkOperator(
            id="ucrlCategoriesRandomWalk",
            parameter="@ucrlRateCategories"
        ).xml,
        SwapOperator(
            id="ucrlCategoriesSwap",
            parameter="@ucrlRateCategories"
        ).xml,
        UniformOperator(
            id="ucrlCategoriesUniform",
            parameter="@ucrlRateCategories"
        ).xml

    ])
    assert ucrl_clock.xml_updown_operator == UpDownOperator(
        id="ucrlMeanUpDownOperator",
        up_parameter="@ucrlMean",
        down_parameter="@Tree"
    ).xml

    ucrl_clock_fixed = UCRLClock(
        prior=[ucrl_mean_prior, ucrl_sd_prior],
        fixed=True
    )
    assert ucrl_clock_fixed.xml_scale_operator == ''
    assert ucrl_clock_fixed.xml_updown_operator == ''
