from critter.blocks.operators import Operator
from critter.blocks.operators import ScaleOperator
from critter.blocks.operators import IntegerRandomWalkOperator
from critter.blocks.operators import SwapOperator
from critter.blocks.operators import UniformOperator
from critter.blocks.operators import UpDownOperator


def test_base_operator_create_success():
    """
    GIVEN: Base operator model with valid parameters
    WHEN:  Operator instance is created
    THEN:  Operator instance is created with valid default parameters
    """
    op = Operator(
        id="test",
        spec="test"
    )
    assert op.xml == \
        '<operator ' \
        'id="test" ' \
        'spec="test"/>'
    assert str(op) == op.xml


def test_scale_operator_create_success():
    """
    GIVEN: Scale operator model with valid parameters
    WHEN:  Operator instance is created
    THEN:  Operator instance is created with valid default parameters
    """
    op = ScaleOperator(
        id="test",
        parameter="@test"
    )
    assert op.xml == \
        '<operator ' \
        'id="test" ' \
        'spec="ScaleOperator" ' \
        'parameter="@test" ' \
        'weight="1.0" ' \
        'scaleFactor="0.5">' \
        '</operator>'


def test_integer_random_walk_operator_create_success():
    """
    GIVEN: Integer Random Walk operator model with valid parameters
    WHEN:  Operator instance is created
    THEN:  Operator instance is created with valid default parameters
    """
    op = IntegerRandomWalkOperator(
        id="test",
        parameter="@test"
    )
    assert op.xml == \
        '<operator ' \
        'id="test" ' \
        'spec="IntRandomWalkOperator" ' \
        'parameter="@test" ' \
        'weight="10.0" ' \
        'windowSize="1">' \
        '</operator>'


def test_swap_operator_create_success():
    """
    GIVEN: Swap operator model with valid parameters
    WHEN:  Operator instance is created
    THEN:  Operator instance is created with valid default parameters
    """
    op = SwapOperator(
        id="test",
        parameter="@test"
    )
    assert op.xml == \
        '<operator ' \
        'id="test" ' \
        'spec="SwapOperator" ' \
        'intparameter="@test" ' \
        'weight="10.0">' \
        '</operator>'


def test_uniform_operator_create_success():
    """
    GIVEN: Uniform operator model with valid parameters
    WHEN:  Operator instance is created
    THEN:  Operator instance is created with valid default parameters
    """
    op = UniformOperator(
        id="test",
        parameter="@test"
    )
    assert op.xml == \
        '<operator ' \
        'id="test" ' \
        'spec="UniformOperator" ' \
        'parameter="@test" ' \
        'weight="10.0">' \
        '</operator>'


def test_up_down_operator_create_success():
    """
    GIVEN: UpDown operator model with valid parameters
    WHEN:  Operator instance is created
    THEN:  Operator instance is created with valid default parameters
    """
    op = UpDownOperator(
        id="test",
        up_idref="test",
        down_idref="tree"
    )
    assert op.xml == \
        '<operator ' \
        'id="test" ' \
        'spec="UpDownOperator" ' \
        'weight="3.0" ' \
        'scaleFactor="0.75">'\
        '<up idref="test" />'\
        '<down idref="tree" />'\
        '</operator>'

