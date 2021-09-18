
from pydantic import BaseModel, ValidationError, root_validator, validator
from critter.blocks.distributions import Distribution
from critter.blocks.parameters import RealParameter
from critter.utils import get_uuid
from critter.errors import CritterError
from math import inf as infinity
from typing import List


class Prior(BaseModel):
    """ Base class for priors """
    id: str = f'Prior.{get_uuid(short=True)}'  # prior identifier prefix defined in all prior subclasses (id="")

    distribution: List[Distribution]  # prior distribution/s, configured
    initial: List[float]
    lower: float = -infinity
    upper: float = infinity
    dimension: int = 1
    sliced: bool = False
    intervals: list = []
    param_spec: str = "parameter.RealParameter"  # changes in MTDB model to IntegerParameter

    def __str__(self):
        return self.xml

    @property
    def xml(self) -> str:
        if not self.sliced:
            # Normal singular prior distribution
            return f'<Prior ' \
                   f'id="{self.id}Prior" ' \
                   f'name="distribution" ' \
                   f'x="@{self.id}">' \
                   f'{self.distribution[0].xml}' \
                   f'</Prior>'
        else:
            # Sliced sampling proportion distribution per interval
            sliced_priors = ''
            for i, distribution in enumerate(self.distribution):
                sliced_priors += f'<Prior ' \
                                 f'id="{self.id}Slice{i+1}" ' \
                                 f'name="distribution" ' \
                                 f'x="@{self.id}{i+1}">' \
                                 f'{distribution.xml}' \
                                 f'</Prior>'
            return sliced_priors

    @property  # alias
    def xml_prior(self) -> str:
        return self.xml

    @property
    def xml_param(self) -> str:
        # Allow for higher dimensions using slices
        initial = " ".join(str(i) for i in self.initial)
        param = RealParameter(  # TODO: validators on RealParameter
            id=f"{self.id}",
            name="stateNode",
            value=initial,
            spec=self.param_spec,
            dimension=self.dimension,
            lower=self.lower,
            upper=self.upper
        )
        return param.xml

    @property
    def xml_logger(self) -> str:
        return f'<log idref="{self.id}"/>'

    # Clock scale operator for priors
    @property
    def xml_scale_operator(self):
        return

    # Sliced priors: slice function, rate change times, and logger
    @property
    def xml_slice_function(self) -> str:
        if not self.sliced:
            return ''
        else:
            xml = ''
            for i, _ in enumerate(self.distribution):
                xml += f'<function spec="beast.core.util.Slice" ' \
                       f'id="{self.id}{i+1}" ' \
                       f'arg="@{self.id}" ' \
                       f'index="{i}" ' \
                       f'count="1"/>\n'
            return xml

    @property
    def xml_slice_rate_change_times(self) -> str:
        if not self.sliced:
            return ''
        else:
            intervals = " ".join(str(i) for i in self.intervals)
            if self.id.startswith('samplingProportion'):
                rate_change_times = 'samplingRateChangeTimes'
            elif self.id.startswith('rho'):
                rate_change_times = 'samplingRateChangeTimes'
            elif self.id.startswith('reproductiveNumber'):
                rate_change_times = 'birthRateChangeTimes'
            elif self.id.startswith('becomeUninfectious'):
                rate_change_times = 'deathRateChangeTimes'
            else:
                raise CritterError(
                    'Rate change times (slices or intervals) are only defined for: '
                    'rho and samplingProportion (<samplingRateChangeTimes/>), '
                    'reproductiveNumber (<birthRateChangeTimes/>) and'
                    'becomeUninfectious (<deathRateChangeTime/>) priors'
                )

            return f'<{rate_change_times} ' \
                   f'spec="beast.core.parameter.RealParameter" ' \
                   f'value="{intervals}"/>\n'

    @property
    def xml_slice_logger(self) -> str:
        if not self.sliced:
            return ''
        else:
            loggers = ''
            for i, _ in enumerate(self.distribution):
                loggers += f'<log idref="{self.id}{i+1}"/>\n'
            return loggers

    @validator("initial")
    def validate_initial_not_empty(cls, v):
        if len(v) == 0:
            raise ValidationError(
                "Initial value(s) must be specified as non-empty list"
            )
        return v

    @validator("distribution")
    def validate_distribution_not_empty(cls, v):
        if len(v) == 0:
            raise ValidationError(
                "Distribution(s) must be specified as non-empty list"
            )
        return v

    @root_validator
    def validate_sliced_config(cls, fields):
        # Slicing only available for birth death models at the moment
        # TODO: slice intervals ordered correctly
        sliced = fields.get('sliced')
        initial = fields.get('initial')
        dimension = fields.get('dimension')
        intervals = fields.get('intervals')
        distribution = fields.get('distribution')

        if sliced and not fields.get('id').startswith(
            ('origin', 'rho', 'samplingProportion', 'reproductiveNumber', 'becomeUninfectious')
        ):
            raise ValidationError(
                'Cannot create a sliced prior that does not belong to a valid birth-death model prior'
            )
        if sliced and dimension <= 1:
            raise ValidationError(
                'A sliced prior cannot have less than two dimensions'
            )
        if sliced and len(initial) != dimension:
            raise ValidationError(
                'Number of initial values in a sliced prior must be equal to the number of dimensions'
            )
        if sliced and len(distribution) != dimension:
            raise ValidationError(
                'Number of distributions in a sliced prior must be equal to the number of dimensions'
            )
        if sliced and not intervals:
            raise ValidationError(
                'In a sliced prior, the list of intervals may not be empty'
            )
        if sliced and len(intervals) != dimension:
            raise ValidationError(
                'Number of slice intervals must be equal to the number of dimensions'
            )
        return fields

    


# Birth-Death Skyline Serial
class OriginPrior(Prior):
    id = "origin"


class ReproductiveNumberPrior(Prior):
    id = "reproductiveNumber"


class SamplingProportionPrior(Prior):
    id = "samplingProportion"


class BecomeUninfectiousRatePrior(Prior):
    id = "becomeUninfectiousRate"


class RhoPrior(Prior):
    id = "rho"


# MultiType BirthDeath Priors /w modifications to SamplingProportion
class RateMatrixPrior(Prior):
    id = "rateMatrix"


class SamplingProportionMultiTypePrior(Prior):
    id = "samplingProportion"

    # Using a distribution component for prior here, not sure why:
    @property
    def xml(self) -> str:
        return f'<distribution ' \
               f'id="{self.id}Prior" ' \
               f'spec="multitypetree.distributions.ExcludablePrior" ' \
               f'x="@{self.id}">' \
               f'<xInclude id="samplingProportionXInclude" ' \
               f'spec="parameter.BooleanParameter" ' \
               f'dimension="{self.dimension}">' \
               f'{self.get_include_string()}' \
               f'</xInclude>' \
               f'{self.distribution[0].xml}' \
               f'</distribution>'

    def get_include_string(self) -> str:
        incl = ['true' if v != 0 else 'false' for v in self.initial]
        return ' '.join(incl)


# Coalescent Bayesian Skyline
class PopulationSizePrior(Prior):
    id = 'bPopSizes'


class GroupSizePrior(Prior):
    id = 'bGroupSizes'
    param_spec = 'parameter.IntegerParameter'

    @property
    def state_node_group_size(self) -> str:
        return f'<stateNode ' \
               f'id="bGroupSizes" ' \
               f'spec="parameter.IntegerParameter" ' \
               f'dimension="{self.dimension}">' \
               f'{self.initial}' \
               f'</stateNode>'


# Clock priors
class ClockRatePrior(Prior):
    id = 'clockRate'


class UCREPrior(Prior):
    id = 'ucreMean'


class UCRLMeanPrior(Prior):
    id = 'ucrlMean'


class UCRLSDPrior(Prior):
    id = 'ucrlSD'
