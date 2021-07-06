import pytest
from critter.errors import CritterError


def test_errors_critter_exception():
    """
    GIVEN:  CritterError base exception
    WHEN:   CritterError base exception is raised
    THEN:   CritterError is raised
    """

    with pytest.raises(CritterError):
        raise CritterError
