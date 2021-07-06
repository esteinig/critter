from critter.blocks.priors import *
from critter.blocks.distributions import Exponential


def test_prior_subclass_create_success():
    """
    GIVEN: Prior subclassess with predefined identifiers and valid defaults
    WHEN:  Prior subclasses are created
    THEN:  Prior subclassses are created with valid default identifiers
    """
    distr, i = [Exponential(mean=0.5)], [1.0]
    assert Origin(distribution=distr, initial=i).id == 'origin'
    assert ReproductiveNumber(distribution=distr, initial=i).id == "reproductiveNumber"
    assert SamplingProportion(distribution=distr, initial=i).id == "samplingProportion"
    assert Rho(distribution=distr, initial=i).id == "rho"
    assert BecomeUninfectiousRate(distribution=distr, initial=i).id == "becomeUninfectiousRate"
    assert RateMatrix(distribution=distr, initial=i).id == "rateMatrix"
    assert PopulationSize(distribution=distr, initial=i).id == "bPopSizes"

    # Test modified XML properties of these two subclasses:
    sp_mtbd = SamplingProportionMTBD(distribution=distr, initial=i)
    ps_coal = GroupSize(distribution=distr, initial=i)
    assert sp_mtbd.id == "samplingProportion"
    assert ps_coal.id == "bGroupSizes"
    assert ps_coal.param_spec == "parameter.IntegerParameter"
    assert ps_coal.state_node_group_size == f'<stateNode id="bGroupSizes" spec="parameter.IntegerParameter" ' \
        f'dimension="{ps_coal.dimension}">{ps_coal.initial}</stateNode>'
    assert sp_mtbd.get_include_string() == (1, 'true')

    _dim, _incl = sp_mtbd.get_include_string()
    _dist = f'<distribution id="{sp_mtbd.id}Prior"' \
            f' spec="multitypetree.distributions.ExcludablePrior"' \
            f' x="@{sp_mtbd.id}">'
    _xinclude = f'<xInclude id="samplingProportionXInclude" ' \
                f'spec="parameter.BooleanParameter" ' \
                f'dimension="{_dim}">{_incl}</xInclude>'
    assert sp_mtbd.xml.startswith(_dist)
    assert _xinclude in sp_mtbd.xml
    assert sp_mtbd.distribution[0].xml in sp_mtbd.xml
    assert sp_mtbd.xml.endswith('</distribution>')
