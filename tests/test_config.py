from critter.config import load_config
from critter.models import BirthDeathSkylineSerial

def test_load_model_strict_sliced_yaml_success(bdss_strict_sliced_yaml_template_ok):
    """
    GIVEN: load_config function with valid template input
    WHEN:  CritterConfig instance is created from template input
    THEN:  CritterConfig instance is created successfully
    """

    
    load_config(yaml_file=bdss_strict_sliced_yaml_template_ok)

def test_load_model_ucre_sliced_yaml_success(bdss_ucre_sliced_yaml_template_ok):
    """
    GIVEN: load_config function with valid template input
    WHEN:  CritterConfig instance is created from template input
    THEN:  CritterConfig instance is created successfully
    """

    
    load_config(yaml_file=bdss_ucre_sliced_yaml_template_ok)

def test_load_model_ucrl_sliced_yaml_success(bdss_ucrl_sliced_yaml_template_ok):
    """
    GIVEN: load_config function with valid template input
    WHEN:  CritterConfig instance is created from template input
    THEN:  CritterConfig instance is created successfully
    """

    
    load_config(yaml_file=bdss_ucrl_sliced_yaml_template_ok)


def test_get_model_strict_sliced_yaml_success(bdss_strict_sliced_yaml_template_ok, critter_ok):
    """
    GIVEN: load_config function with valid bdss template input
    WHEN:  CritterModel instance is created from template input
    THEN:  CritterModel instance is created successfully
    """

    critter_config = load_config(yaml_file=bdss_strict_sliced_yaml_template_ok)
    critter_model = critter_config.get_model(critter=critter_ok)

    assert isinstance(critter_model, BirthDeathSkylineSerial)


def test_get_model_ucre_sliced_yaml_success(bdss_ucre_sliced_yaml_template_ok, critter_ok):
    """
    GIVEN: load_config function with valid bdss template input
    WHEN:  CritterModel instance is created from template input
    THEN:  CritterModel instance is created successfully
    """

    critter_config = load_config(yaml_file=bdss_ucre_sliced_yaml_template_ok)
    critter_model = critter_config.get_model(critter=critter_ok)

    print(critter_model.clock)

    assert isinstance(critter_model, BirthDeathSkylineSerial)

def test_get_model_ucrl_sliced_yaml_success(bdss_ucrl_sliced_yaml_template_ok, critter_ok):
    """
    GIVEN: load_config function with valid bdss template input
    WHEN:  CritterModel instance is created from template input
    THEN:  CritterModel instance is created successfully
    """

    critter_config = load_config(yaml_file=bdss_ucrl_sliced_yaml_template_ok)
    critter_model = critter_config.get_model(critter=critter_ok)

    print(critter_model.clock)

    assert isinstance(critter_model, BirthDeathSkylineSerial)
