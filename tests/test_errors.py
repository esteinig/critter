import pytest
from critter.errors import CritterError


def test_errors_critter_exception():
    """
    GIVEN:  Critter baser exception
    WHEN:   Critter baser exception is raised
    THEN:   CritterError is raised
    """

    with pytest.raises(CritterError):
        raise CritterError
