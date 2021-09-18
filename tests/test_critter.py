

import jinja2
from pandas import DataFrame
from pytest import raises
from critter.critter import Critter
from critter.errors import CritterError


def test_critter_base_data_ok_success(
    critter_dates_ok, critter_alignment_ok, critter_reference_ok, 
    critter_date_xml, critter_alignment_xml, critter_run_xml_mcmc, critter_run_xml_mcmcmc
):
    """
    GIVEN: Critter instance with valid data inputs
    WHEN:  Critter instance is created
    THEN:  Critter instance is created with valid defaults
    """

    true_dates = DataFrame(
        {'name': ['seq1', 'seq2', 'seq3'], 'date': [2015.12, 2016.12, 2017.12]}
    )
    true_ref = {'ref': 'ACTGNCTG'}
    true_aln = {'seq1': 'ACTG', 'seq2': 'ACTG', 'seq3': 'ACTG'}

    crit = Critter(
        date_file=critter_dates_ok, 
        alignment_file=critter_alignment_ok, 
        reference_file=critter_reference_ok
    )

    assert crit.dates.equals(true_dates)
    assert crit.reference == true_ref
    assert crit.alignment == true_aln

    assert crit.xml_alignment == critter_alignment_xml
    assert crit.xml_dates == critter_date_xml
    assert crit.xml_run == critter_run_xml_mcmc

    crit.chain_type = 'coupled'
    assert crit.xml_run == critter_run_xml_mcmcmc


def test_critter_base_data_dates_fail(
    critter_dates_bad1, critter_dates_bad2, critter_alignment_ok, critter_reference_ok
):
    """
    GIVEN: Critter instance with invalid date file inputs
    WHEN:  Critter instance is created
    THEN:  Critter instance creation fails with CritterError
    """

    with raises(CritterError) as e:
        Critter(
            date_file=critter_dates_bad1, 
            alignment_file=critter_alignment_ok, 
            reference_file=critter_reference_ok
        )

        assert 'does not have a date' in str(e).lower()
    
    with raises(CritterError) as e:
        Critter(
            date_file=critter_dates_bad2, 
            alignment_file=critter_alignment_ok, 
            reference_file=critter_reference_ok
        )

        assert 'missing data' in str(e).lower()


def test_critter_base_data_fasta_fail(
    critter_dates_ok, critter_alignment_bad, critter_reference_ok
):
    """
    GIVEN: Critter instance with invalid sequence file inputs
    WHEN:  Critter instance is created
    THEN:  Critter instance creation fails with CritterError
    """

    with raises(CritterError) as e:
        Critter(
            date_file=critter_dates_ok, 
            alignment_file=critter_alignment_bad, 
            reference_file=critter_reference_ok
        )

        assert 'contains base other than' in str(e).lower()
    

def test_critter_base_load_template_success(
    critter_dates_ok, critter_alignment_ok, critter_reference_ok
):
    """
    GIVEN: Critter instance with valid inputs
    WHEN:  Critter instance template method is called (jinja2)
    THEN:  Critter instance template is loaded (jinja2)
    """

    crit = Critter(
        date_file=critter_dates_ok, 
        alignment_file=critter_alignment_ok, 
        reference_file=critter_reference_ok
    )

    template = crit.load_template(name='bdss.xml')

    assert isinstance(template, jinja2.Template)

