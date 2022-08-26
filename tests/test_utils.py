from critter.utils import get_uuid


def test_utils_get_uuid():
    """
    GIVEN:  utility function get_uuid() with valid params
    WHEN:   utility function get_uuid() is called
    THEN:   a valid full length or short UUID string is returned
    """
    full = get_uuid()
    short = get_uuid(short=True)
    assert type(full) == str
    assert type(short) == str
    assert len(full) == 36
    assert len(short) == 8


def test_version_var():
    """
    GIVEN:  version variable defined in package
    WHEN:   importing __version__
    THEN:   a valid version string is returned
    """
    from critter.version import __version__
    assert type(__version__) == str
