from critter.blocks.base import Prior


class Rate(Prior):
    slice_id = 'rate'
    prior_id = 'ClockPrior'
    param_id = 'clockRate'


class UCED(Prior):
    slice_id = 'uced'
    prior_id = 'UCMeanRatePrior'
    param_id = 'ucedMean'


class UCLDMean(Prior):
    slice_id = 'ucld_mean'
    prior_id = 'MeanRatePrior'
    param_id = 'ucldMean'


class UCLDSD(Prior):
    slice_id = 'ucld_sd'
    prior_id = 'ucldStdevPrior'
    param_id = 'ucldStdev'


# Model priors for Birth-Death Skyline Serial
class Origin(Prior):
    slice_id = 'origin'
    prior_id = 'originPrior_BDSKY_Serial'
    param_id = 'origin_BDSKY_Serial'


class ReproductiveNumberBDSS(Prior):
    slice_id = 'reproductiveNumber'
    prior_id = 'reproductiveNumberPrior_BDSKY_Serial'
    param_id = 'reproductiveNumber_BDSKY_Serial'


class SamplingProportionBDSS(Prior):
    slice_id = 'samplingProportion'
    prior_id = 'samplingProportionPrior_BDSKY_Serial'
    param_id = 'samplingProportion_BDSKY_Serial'


class BecomeUninfectiousBDSS(Prior):
    slice_id = 'becomeUninfectious'
    prior_id = 'becomeUninfectiousRatePrior_BDSKY_Serial'
    param_id = 'becomeUninfectiousRate_BDSKY_Serial'


# Contemporary model priors
class OriginBDSC(Prior):
    slice_id = 'origin'
    prior_id = 'originPrior_BDSKY_Contempt'
    param_id = 'origin_BDSKY_Contemp'


class ReproductiveNumberBDSC(Prior):
    slice_id = 'reproductiveNumber'
    prior_id = 'reproductiveNumberPrior_BDSKY_Contemp'
    param_id = 'reproductiveNumber_BDSKY_Contemp'


class RhoBDSC(Prior):
    slice_id = 'rho'
    prior_id = 'rhoPrior_BDSKY_Contemp'
    param_id = 'rho_BDSKY_Contemp'


class BecomeUninfectiousBDSC(Prior):
    slice_id = 'becomeUninfectious'
    prior_id = 'becomeUninfectiousRatePrior_BDSKY_Contemp'
    param_id = 'becomeUninfectiousRate_BDSKY_Contemp'


# MultiType BirthDeath Priors
class ReproductiveNumberMTBD(Prior):
    prior_id = 'RPrior'
    param_id = 'R0'


class SamplingProportionMTBD(Prior):
    prior_id = 'samplingProportionPrior'
    param_id = 'samplingProportion'

    # Using a distribution component for prior here, not sure why:
    @property
    def xml(self) -> str:
        dim, incl = self._get_include_string()
        return f"""
        <distribution id="{self.prior_id}" spec="multitypetree.distributions.ExcludablePrior" x="@{self.param_id}">
        <xInclude id="samplingProportionXInclude" spec="parameter.BooleanParameter" dimension="{dim}">{incl}</xInclude>
        {self.distribution.xml}
        </distribution>
        """

    def _get_include_string(self) -> (int, str):
        incl = []
        for v in self.initial:
            if v != 0:
                incl.append('true')
            else:
                incl.append('false')

        return len(self.initial), '' ''.join(incl)


class BecomeUninfectiousMTBD(Prior):
    prior_id = 'becomeUninfectiousRatePrior'
    param_id = 'becomeUninfectiousRate'


class RateMatrix(Prior):
    prior_id = 'rateMatrixPrior'
    param_id = 'rateMatrix'


# Model priors for Coalescent Bayesian Skyline

class PopulationSize(Prior):
    slice_id = 'bPopSizes'
    prior_id = ''  # no XML prior necessary  # todo: check if break compatibility, changed to '' from None
    param_id = 'bPopSizes'


class GroupSize(Prior):
    slice_id = 'bGroupSizes'
    prior_id = ''  # no XML prior necessary
    param_id = 'bGroupSizes'
    param_spec = 'parameter.IntegerParameter'

    @property
    def state_node_group_size(self):

        return f'<stateNode id="bGroupSizes" spec="parameter.IntegerParameter" ' \
            f'dimension="{self.dimension}">{self.initial}</stateNode>'
