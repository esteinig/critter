from critter.blocks.base import Prior


# Birth-Death Skyline Serial
class Origin(Prior):
    id = "origin"


class ReproductiveNumber(Prior):
    id = "reproductiveNumber"


class SamplingProportion(Prior):
    id = "samplingProportion"


class BecomeUninfectiousRate(Prior):
    id = "becomeUninfectiousRate"


class Rho(Prior):
    id = "rho"


# MultiType BirthDeath Priors /w modifications to SamplingProportion
class RateMatrix(Prior):
    id = "rateMatrix"


class SamplingProportionMTBD(Prior):
    id = "samplingProportion"

    # Using a distribution component for prior here, not sure why:
    @property
    def xml(self) -> str:
        dim, incl = self.get_include_string()
        return f'<distribution id="{self.id}Prior" ' \
               f'spec="multitypetree.distributions.ExcludablePrior" x="@{self.id}">' \
               f'<xInclude id="samplingProportionXInclude" spec="parameter.BooleanParameter" dimension="{dim}">' \
               f'{incl}</xInclude>{self.distribution[0].xml}</distribution>'

    def get_include_string(self) -> (int, str):
        incl = ['true' if v != 0 else 'false' for v in self.initial]
        return len(self.initial), ' '.join(incl)


# Coalescent Bayesian Skyline
class PopulationSize(Prior):
    id = 'bPopSizes'


class GroupSize(Prior):
    id = 'bGroupSizes'
    param_spec = 'parameter.IntegerParameter'

    @property
    def state_node_group_size(self) -> str:
        return f'<stateNode id="bGroupSizes" spec="parameter.IntegerParameter" ' \
            f'dimension="{self.dimension}">{self.initial}</stateNode>'


# Clock priors
class Rate(Prior):
    id = 'clockRate'


class UCED(Prior):
    id = 'ucedMeanRate'


class UCLDMean(Prior):
    id = 'ucldMeanRate'


class UCLDSD(Prior):
    id = 'ucldSD'