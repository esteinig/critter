""" Base blocks mirroring BEAST 2.5 """

from math import inf as infinity
from pydantic import BaseModel, Extra, root_validator
from typing import List
from critter.errors import CritterError
from critter.utils import get_uuid


class RealParameter(BaseModel):
    """ <parameter/> """
    id: str
    name: str
    value: float
    lower: float = -infinity
    upper: float = +infinity
    dimension: int = 1
    estimate: bool = False
    spec: str = "parameter.RealParameter"

    def __str__(self):
        return self.xml

    @property
    def xml(self):
        return f'<parameter id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'estimate="{str(self.estimate).lower()}" ' \
               f'lower="{str(self.lower)}" ' \
               f'upper="{str(self.upper)}" ' \
               f'name="{self.name}">{self.value}' \
               f'</parameter>'


class Distribution(BaseModel, extra=Extra.allow):
    """ Distribution base class """
    id: str = f'Distribution.{get_uuid(short=True)}'
    # parameters defined in subclasses as RealParameters
    # this let's users config the parameter block id
    params: List[RealParameter] = list()
    # optional sub model pythonic attributes -> original name
    _attr_name = {
        'real_space': 'meanInRealSpace',
        'mode': 'mode'
    }

    def __str__(self):
        return self.xml

    @property
    def xml(self):
        _param_block = "".join([str(param) for param in self.params])
        return f'<{self.__class__.__name__} id="{self.id}" ' \
               f'{self._get_distr_config()} name="distr">' \
               f'{_param_block}</{self.__class__.__name__}>'

    def _get_distr_config(self) -> str:
        """ Get optional distribution configs from subclasses """
        return ' '.join([
            f'{self._attr_name[attr]}="{value}"'
            for attr, value in vars(self).items()
            if attr in self._attr_name.keys()
        ])


class Prior(BaseModel):
    """ Base class for priors """
    id: str = f'Prior.{get_uuid(short=True)}'  # prior identifier prefix defined in all prior subclasses (id="")
    distribution: List[Distribution]  # prior distribution, configured
    initial: list  # initial values for the prior param

    lower: float = -infinity  # lower bound for the prior param
    upper: float = infinity   # upper bound for the prior param
    dimension: int = 1        # dimension of the prior param

    sliced: bool = False  # for sliced SamplingProportion prior
    intervals: list = []  # for sliced SamplingProportion prior

    scw: str = None  # scale operator weight defined in clock subclasses
    scx: str = None  # scale identifier defined in clock subclasses
    param_spec: str = "parameter.RealParameter"  # changes in MTDB model to IntegerParameter

    @property
    def xml(self) -> str:
        if not self.sliced:
            # Normal singular prior distribution
            return f'<prior id="{self.id}Prior" name="distribution" ' \
                   f'x="@{self.id}">{self.distribution[0].xml}</prior>'
        else:
            # Sliced sampling proportion distribution per interval
            sliced_priors = ''
            for i, distribution in enumerate(self.distribution):
                sliced_priors += f'<prior id="{self.id}Slice{i+1}" name="distribution" ' \
                                 f'x="@{self.id}{i+1}">{distribution.xml}</prior>'
            return sliced_priors

    @property  # alias
    def xml_prior(self) -> str:
        return self.xml

    @property
    def xml_param(self) -> str:
        # Allow for higher dimensions using slices
        initial = " ".join(str(i) for i in self.initial) if len(self.initial) > 1 else self.initial[0]
        param = RealParameter(  # TODO: validators on RealParameter
            id=f"{self.id}", name="stateNode", value=initial, spec=self.param_spec,
            dimension=self.dimension, lower=self.lower, upper=self.upper
        )
        return str(param)

    @property
    def xml_logger(self) -> str:
        return f'<log idref="{self.id}"/>'

    # Clock scale operator for priors
    @property
    def xml_scale_operator(self):
        return

    # Sliced priors
    @property
    def xml_slice_function(self) -> str:
        if not self.sliced:
            return ''
        else:
            xml = ''
            for i, _ in enumerate(self.distribution):
                xml += f'<function spec="beast.core.util.Slice" id="{self.id}{i+1}" ' \
                    f'arg="@{self.id}" index="{i}" count="1"/>\n'
            return xml

    @property
    def xml_slice_rate(self) -> str:
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

            return f'<{rate_change_times} spec="beast.core.parameter.RealParameter" value="{intervals}"/>'

    @property
    def xml_slice_logger(self) -> str:
        if not self.sliced:
            return ''
        else:
            loggers = ''
            for i, value in enumerate(self.distribution):
                loggers += f'<log idref="{self.id}{i+1}"/>\n'
            return loggers

    @root_validator
    def validate_sliced_id(cls, values):
        # Slicing only available for a subset of priors (BD Sky models)
        if values.get('sliced') and not values.get('id').startswith(
            ('origin', 'rho', 'samplingProportion', 'reproductiveNumber', 'becomeUninfectious')
        ):
            raise CritterError('Cannot create a sliced prior that does not belong to valid birth-death models')
        else:
            return values


class Operator(BaseModel):
    """ <operator/> """
    pass


# def check_init(self):
#
#     # Initial value checks
#     if self.initial in self.allowed_negative_infinity \
#             or self.initial in self.allowed_positive_infinity:
#         raise BeastlingError(
#             f'Initial value cannot be: {self.initial}'
#         )
#
#     if isinstance(self.initial, list):
#         try:
#             self.initial = [float(i) for i in self.initial]
#         except TypeError:
#             raise BeastlingError(
#                 f'Initial values in list must be valid floats'
#             )
#     else:
#         try:
#             if self.param_spec == "parameter.RealParameter":
#                 self.initial = float(self.initial)
#             elif self.param_spec == "parameter.IntegerParameter":
#                 self.initial = int(self.initial)
#             else:
#                 raise BeastlingError(
#                     f'Parameter specification: `{self.param_spec}` not found'
#                 )
#         except TypeError:
#             raise BeastlingError(
#                 f'Initial value must be a valid float'
#             )
#
#     try:
#         self.intervals = [float(i) for i in self.intervals]
#     except TypeError:
#         raise BeastlingError(
#             f'Interval values in list must be valid floats'
#         )
#
#     if self.lower is not None or self.upper is not None:
#         # Upper / lower infinity checks
#         if self.lower in self.allowed_positive_infinity:
#             raise BeastlingError(
#                 f'Lower bound cannot be positive infinity'
#             )
#
#         if self.upper in self.allowed_negative_infinity:
#             raise BeastlingError(
#                 f'Upper bound cannot be negative infinity'
#             )
#
#         # Upper / lower value checks and conversion
#         if self.lower in self.allowed_negative_infinity:
#             self.lower = -math.inf
#         else:
#             try:
#                 self.lower = float(self.lower)
#             except TypeError:
#                 raise BeastlingError(
#                     'Lower bound value must be valid float or infinity string'
#                 )
#
#         if self.upper in self.allowed_positive_infinity:
#             self.upper = math.inf
#         else:
#             try:
#                 self.upper = float(self.upper)
#             except TypeError:
#                 raise BeastlingError(
#                     'Upper bound value must be valid float or infinity string'
#                 )
#
#         # Initital bounds check
#         if isinstance(self.initial, list):
#             check_initial = self.initial
#         else:
#             check_initial = [self.initial]
#
#         for i in check_initial:
#             if not self.lower <= i <= self.upper:
#                 raise BeastlingError(
#                     f'Initial value {i} must be within '
#                     f'bounds: {self.lower} and {self.upper}'
#                 )
#
#     if self.sliced:
#         if not isinstance(self.initial, list):
#             raise BeastlingError(
#                 'Something went wrong, slices set but '
#                 'initial values is not a list'
#             )
#
#         if self.dimension != len(self.initial) or \
#                 self.dimension != len(self.intervals):
#             raise BeastlingError(
#                 'In sliced SamplingProportion, the number of dimensions '
#                 'must match the number of initial values and intervals'
#             )
#
#         if len(self.initial) != len(self.intervals):
#             raise BeastlingError(
#                 'Length of initial values must be the same length of '
#                 'intervals when setting intervals of sampling proportion'
#             )