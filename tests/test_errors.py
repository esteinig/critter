from pytest import raises
from critter.errors import CritterError


def test_errors_critter_exception():
    """
    GIVEN:  CritterError base exception
    WHEN:   CritterError base exception is raised
    THEN:   CritterError is raised
    """
    with raises(CritterError):
        raise CritterError
