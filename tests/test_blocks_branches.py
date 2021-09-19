from critter.blocks.branches import BranchRateModel
from critter.blocks.distributions import Exponential


def test_branch_rate_model_create_success():
    """
    GIVEN: BranchRateModel model with valid parameters
    WHEN:  BranchRateModel instance is created
    THEN:  BranchRateModel instance is created with valid default parameters
    """

    # Default base class construction
    brm = BranchRateModel(
        id='test',
        spec='test',
        parameter="@test"
    )
    # note space after clock.rate
    assert brm.xml == '<branchRateModel ' \
        'id="test" ' \
        'spec="test" ' \
        'clock.rate="@test" >' \
        '</branchRateModel>'
    assert str(brm) == brm.xml

    # Default base class without a distribution
    brm = BranchRateModel(
        id='test',
        spec='test',
        parameter="@test",
        tree_parameter="@tree",
        rate_categories_parameter="@"
    )
    # note space after clock.rate
    assert brm.xml == '<branchRateModel ' \
        'id="test" ' \
        'spec="test" ' \
        'clock.rate="@test" >' \
        '</branchRateModel>'

    # Default base class with distribution
    exp = Exponential(mean=1.0)
    brm = BranchRateModel(
        id='test',
        spec='test',
        parameter="@test",
        distribution=exp,
        tree_parameter="@tree",
        rate_categories_parameter="@rateCategories"
    )
    assert brm.xml == '<branchRateModel ' \
        'id="test" ' \
        'spec="test" ' \
        'clock.rate="@test" ' \
        'rateCategories="@rateCategories" ' \
        'tree="@tree">' \
        f'{exp.xml}' \
        '</branchRateModel>'


