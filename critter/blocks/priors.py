from critter.blocks.base import Prior


class Rate(Prior):
    name = 'rate'
    idx = "ClockPrior.c"
    x = "clockRate.c"


class UCED(Prior):
    name = 'uced'
    idx = "UCMeanRatePrior.c"
    x = "ucedMean.c"


class UCLDMean(Prior):
    name = 'ucld_mean'
    idx = "MeanRatePrior.c"
    x = "ucldMean.c"


class UCLDSD(Prior):
    name = 'ucld_sd'
    idx = "ucldStdevPrior.c"
    x = "ucldStdev.c"


# Model priors for Birth-Death Skyline Serial
class Origin(Prior):
    name = "origin"
    idx = f"originPrior_BDSKY_Serial.t"
    x = f"origin_BDSKY_Serial.t"


class ReproductiveNumberBDSS(Prior):
    name = "reproductiveNumber"
    idx = "reproductiveNumberPrior_BDSKY_Serial.t"
    x = "reproductiveNumber_BDSKY_Serial.t"


class SamplingProportionBDSS(Prior):
    name = 'samplingProportion'
    idx = "samplingProportionPrior_BDSKY_Serial.t"
    x = "samplingProportion_BDSKY_Serial.t"


class BecomeUninfectiousBDSS(Prior):
    name = 'becomeUninfectious'
    idx = "becomeUninfectiousRatePrior_BDSKY_Serial.t"
    x = "becomeUninfectiousRate_BDSKY_Serial.t"


# Contemporary model priors
class OriginBDSC(Prior):
    name = "origin"
    idx = f"originPrior_BDSKY_Contempt"
    x = f"origin_BDSKY_Contemp.t"


class ReproductiveNumberBDSC(Prior):
    name = "reproductiveNumber"
    idx = "reproductiveNumberPrior_BDSKY_Contemp.t"
    x = "reproductiveNumber_BDSKY_Contemp.t"


class RhoBDSC(Prior):
    name = 'rho'
    idx = "rhoPrior_BDSKY_Contemp.t"
    x = "rho_BDSKY_Contemp.t"


class BecomeUninfectiousBDSC(Prior):
    name = 'becomeUninfectious'
    idx = "becomeUninfectiousRatePrior_BDSKY_Contemp.t"
    x = "becomeUninfectiousRate_BDSKY_Contemp.t"


# MultiType BirthDeath Priors
class ReproductiveNumberMTBD(Prior):
    idx = "RPrior.t"
    x = "R0.t"


class SamplingProportionMTBD(Prior):
    idx = "samplingProportionPrior.t"
    x = "samplingProportion.t"

    # Using a distribution component for prior here, not sure why:
    @property
    def xml(self) -> str:
        dim, incl = self.get_include_string()
        return f"""
        <distribution id="{self.idx}:snp" spec="multitypetree.distributions.ExcludablePrior" x="@{self.x}:snp">
            <xInclude id="samplingProportionXInclude.t:snp" spec="parameter.BooleanParameter" dimension="{dim}">{incl}</xInclude>
            {self.distribution.get_xml()}
        </distribution>
        """

    def get_include_string(self) -> (int, str):
        incl = []
        for v in self.initial:
            if v != 0:
                incl.append('true')
            else:
                incl.append('false')

        return len(self.initial), " ".join(incl)


class BecomeUninfectiousMTBD(Prior):
    idx = "becomeUninfectiousRatePrior.t"
    x = "becomeUninfectiousRate.t"


class RateMatrix(Prior):
    idx = "rateMatrixPrior.t"
    x = "rateMatrix.t"


# Model priors for Coalescent Bayesian Skyline

class PopulationSize(Prior):
    name = 'bPopSizes'
    idx = ''  # no XML prior necessary  # todo: check if break compatibility, changed to '' from None
    x = "bPopSizes.t"


class GroupSize(Prior):
    name = 'bGroupSizes'
    idx = ''  # no XML prior necessary
    x = "bGroupSizes.t"
    param_spec = "parameter.IntegerParameter"

    @property
    def state_node_group_size(self):

        return f'<stateNode id="bGroupSizes.t:snp" spec="parameter.IntegerParameter" ' \
            f'dimension="{self.dimension}">{self.initial}</stateNode>'
