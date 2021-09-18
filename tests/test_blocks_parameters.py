from pytest import raises

from math import inf as infinity
from pydantic import ValidationError
from critter.blocks.parameters import RealParameter


def test_real_parameter_create_success():
    """
    GIVEN: RealParameter with valid name and value
    WHEN:  RealParameter instance is created
    THEN:  RealParameter instance is created with valid defaults
    """
    param = RealParameter(
        id="test",
        name="alpha",
        value=1.0
    )
    assert param.id == 'test'
    assert param.name == 'alpha'
    assert param.value == '1.0'  # --> see class comments on why
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
    # Required is null
    with raises(ValidationError):
        RealParameter(
            id=None,
            name="alpha",
            value=1.0
        )
    with raises(ValidationError):
        RealParameter(
            id='test',
            name=None,
            value=1.0
        )
    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha",
            value=None
        )
    # Missing required
    with raises(ValidationError):
        RealParameter(
            name="alpha",
            value=1.0
        )
    with raises(ValidationError):
        RealParameter(
            id='test',
            value=1.0
        )
    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha"
        )
    # Defaults changed to null
    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha",
            value=1.0,
            dimension=None
        )
    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha",
            value=1.0,
            estimate=None
        )
    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha",
            value=1.0,
            lower=None
        )
    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha",
            value=1.0,
            upper=None
        )


def test_real_parameter_default_xml_string():
    """
    GIVEN: RealParameter with valid name and value
    WHEN:  RealParameter instance calls __str__
    THEN:  RealParameter instance returns valid XML string
    """
    xml = str(
        RealParameter(
            id='test',
            name="alpha",
            value=1.0
        )
    )
    valid_xml = f'<parameter ' \
                f'id="test" ' \
                f'spec="parameter.RealParameter" ' \
                f'estimate="false" ' \
                f'lower="-inf" ' \
                f'upper="inf" ' \
                f'name="alpha">' \
                f'1.0' \
                f'</parameter>'
    assert xml == valid_xml


def test_real_parameter_string_value_validation_success():
    """
    GIVEN: RealParameter with valid name and floatable string value 
        or values as white space separated string
    WHEN:  RealParameter instance is initiated
    THEN:  RealParameter instance is initiated
    """

    RealParameter(
        id='test',
        name="alpha",
        value="1.0"
    )
    RealParameter(
        id='test',
        name="alpha",
        value="1.0 1.0"
    )
    RealParameter(
        id='test',
        name="alpha",
        value="1.0 1"
    )
    RealParameter(
        id='test',
        name="alpha",
        value="10 10"
    )

def test_real_parameter_string_value_validation_failure():
    """
    GIVEN: RealParameter with valid name and non floatable string value 
        or values as white space separated string
    WHEN:  RealParameter instance is initiated
    THEN:  RealParameter instance is not initiated
    """

    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha",
            value="test"
        )
    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha",
            value="1.0 test"
        )
    
    with raises(ValidationError):
        RealParameter(
            id='test',
            name="alpha",
            value="10 test"
        )