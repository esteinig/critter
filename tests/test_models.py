from critter.models import BirthDeathSkylineSerial
from critter.critter import Critter
from pathlib import Path

def test_model_bdss_success(
    tmpdir, 
    critter_ok,
    bdss_strict_clock_model, 
    bdss_origin_prior, 
    bdss_sampling_proportion_prior_sliced,
    bdss_sampling_proportion_prior, 
    bdss_reproductive_number_prior, 
    bdss_become_uninfectious_rate_prior
):
    """
    GIVEN: BirthDeathSkylineSerial instance with valid input data
    WHEN:  BirthDeathSkylineSerial instance is configured with valid priors and clock model
    THEN:  BirthDeathSkylineSerial instance is configured correctly
    """


    # sliced sampling proportion prior
    bdss = BirthDeathSkylineSerial(
        critter=critter_ok,
        clock=bdss_strict_clock_model,
        origin=bdss_origin_prior,
        sampling_proportion=bdss_sampling_proportion_prior_sliced,
        reproductive_number=bdss_reproductive_number_prior,
        become_uninfectious_rate=bdss_become_uninfectious_rate_prior
    )
    bdss.write(
        xml_file=Path(
            tmpdir.join('bdss_slice.xml')
        )
    )
    # non sliced sampling proportion prior
    bdss = BirthDeathSkylineSerial(
        critter=critter_ok,
        clock=bdss_strict_clock_model,
        origin=bdss_origin_prior,
        sampling_proportion=bdss_sampling_proportion_prior,
        reproductive_number=bdss_reproductive_number_prior,
        become_uninfectious_rate=bdss_become_uninfectious_rate_prior
    )
    bdss.write(
        xml_file=Path(
            tmpdir.join('bdss_no_slice.xml')
        )
    )


def test_model_bdss_slice_xml_function_success(
    critter_ok,
    bdss_strict_clock_model, 
    bdss_origin_prior,
    bdss_sampling_proportion_prior, 
    bdss_sampling_proportion_prior_sliced, 
    bdss_reproductive_number_prior, 
    bdss_become_uninfectious_rate_prior,
    bdss_sampling_proportion_slice_function_xml, 
    bdss_sampling_proportion_slice_logger_xml,
    bdss_sampling_proportion_slice_rate_change_times_xml
):
    """
    GIVEN: BirthDeathSkylineSerial instance with valid input data
    WHEN:  BirthDeathSkylineSerial slice getter with valid priors is called
    THEN:  BirthDeathSkylineSerial slice blocks are returned correctly
    """


    bdss = BirthDeathSkylineSerial(
        critter=critter_ok,
        clock=bdss_strict_clock_model,
        origin=bdss_origin_prior,
        sampling_proportion=bdss_sampling_proportion_prior_sliced,
        reproductive_number=bdss_reproductive_number_prior,
        become_uninfectious_rate=bdss_become_uninfectious_rate_prior
    )

    # No sliced configuration
    xml_slice_functions, \
    xml_slice_rate_change_times, \
    xml_slice_loggers = bdss.get_slice_xmls(
        priors=(
            bdss_reproductive_number_prior, 
            bdss_become_uninfectious_rate_prior, 
            bdss_sampling_proportion_prior
        )
    )
    assert xml_slice_functions == ""
    assert xml_slice_loggers == ""
    assert xml_slice_rate_change_times == ""

    # Sliced configuration
    xml_slice_functions, \
    xml_slice_rate_change_times, \
    xml_slice_loggers = bdss.get_slice_xmls(
        priors=(
            bdss_reproductive_number_prior, 
            bdss_become_uninfectious_rate_prior, 
            bdss_sampling_proportion_prior_sliced
        )
    )
    assert xml_slice_functions == bdss_sampling_proportion_slice_function_xml
    assert xml_slice_loggers == bdss_sampling_proportion_slice_logger_xml
    assert xml_slice_rate_change_times == bdss_sampling_proportion_slice_rate_change_times_xml