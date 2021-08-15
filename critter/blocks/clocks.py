from critter.blocks.operators import SwapOperator, ScaleOperator, IntegerRandomWalkOperator, UniformOperator, UpDownOperator
from critter.blocks.branches import UCREBranchRateModel, UCRLBranchRateModel, StrictBranchRateModel
from critter.blocks.priors import Prior, ClockRatePrior, UCREPrior, UCRLMeanPrior, UCRLSDPrior
from pydantic import BaseModel, ValidationError, validator
from critter.utils import get_uuid
from typing import List


class Clock(BaseModel):
    """ Base class for clock models """
    id: str = f'Clock.{get_uuid(short=True)}'

    prior: List[Prior]
    fixed: bool = False
    state_node: str = ''  # defined in some clock subclasses

    def __str__(self):
        return self.xml

    # Combine multiple prior XMLs
    @property
    def xml(self):
        return self.xml_prior

    @property
    def xml_prior(self):
        return "\n".join([p.xml_prior for p in self.prior])

    @property
    def xml_param(self):
        return "\n".join([p.xml_param for p in self.prior])

    @property
    def xml_logger(self):
        return "\n".join([p.xml_logger for p in self.prior])

    @property
    def xml_state_node(self):
        return self.state_node

    # Defined in clock subclasses
    @property
    def xml_scale_operator(self) -> str:
        return ''

    @property
    def xml_updown_operator(self) -> str:
        return ''

    @property
    def xml_branch_rate_model(self) -> str:
        return ''

    @validator('prior')
    def prior_must_be_clock_prior(cls, field):
        for prior in field:
            if not isinstance(
                prior, (ClockRatePrior, UCREPrior, UCRLMeanPrior, UCRLSDPrior)
            ):
                raise ValidationError(
                    "Clocks must be populated with valid clock prior instances of: "
                    "ClockRate, UCREPrior, UCRLMeanPrior or UCRLSDPrior"
                )
        return field


class StrictClock(Clock):

    @property
    def xml_branch_rate_model(self) -> str:
        return StrictBranchRateModel(
            id="strictClockBranchRate",
            parameter="@clockRate"
        ).xml

    @property
    def xml_scale_operator(self) -> str:
        if self.fixed:
            return ""
        else:
            return ScaleOperator(
                id="strictClockScaleOperator",
                parameter="@clockRate"
            ).xml

    @property
    def xml_updown_operator(self) -> str:
        if self.fixed:
            return ""
        else:
            return UpDownOperator(
                id="strictClockUpDownOperator",
                up_parameter="@clockRate",
                down_parameter="@Tree"
            ).xml


class UCREClock(Clock):
    state_node = f'<stateNode ' \
                 f'id="ucreRateCategories" ' \
                 f'spec="parameter.IntegerParameter" ' \
                 f'dimension="718">' \
                 f'1' \
                 f'</stateNode>'

    @property
    def xml_branch_rate_model(self) -> str:
        return UCREBranchRateModel(
            id="ucreBranchRateModel",
            parameter="@ucreMean",
            tree_parameter="@Tree",
            rate_categories_parameter="@ucreRateCategories"
        ).xml

    @property
    def xml_scale_operator(self) -> str:
        if self.fixed:
            return ''
        else:
            # With default value configurations (should be ok for sensible template)
            operators = [
                ScaleOperator(
                    id="ucreMeanScaleOperator",
                    parameter="@ucreMean"
                ).xml,
                IntegerRandomWalkOperator(
                    id="ucreCategoriesRandomWalk",
                    parameter="@ucreRateCategories"
                ).xml,
                SwapOperator(
                    id="ucreCategoriesSwap",
                    parameter="@ucreRateCategories"
                ).xml,
                UniformOperator(
                    id="ucreCategoriesUniform",
                    parameter="@ucreRateCategories"
                ).xml
            ]
            return "\n".join(operators)

    @property
    def xml_updown_operator(self) -> str:
        if self.fixed:
            return ''
        else:
            return UpDownOperator(
                id="ucreMeanUpDownOperator",
                up_parameter="@ucreMean",
                down_parameter="@Tree"
            ).xml


class UCRLClock(Clock):
    state_node = f'<stateNode ' \
                 f'id="ucrlRateCategories" ' \
                 f'spec="parameter.IntegerParameter" ' \
                 f'dimension="718">' \
                 f'1' \
                 f'</stateNode>'

    @property
    def xml_branch_rate_model(self) -> str:
        return UCRLBranchRateModel(
            id="ucrlBranchRateModel",
            parameter="@ucrlMean",
            rate_categories_parameter="@ucrlRateCategories",
            tree_parameter="@Tree"
        ).xml

    @property
    def xml_scale_operator(self) -> str:
        if self.fixed:
            return ""
        else:
            operators = [
                ScaleOperator(
                    id="ucrlMeanScaleOperator",
                    parameter="@ucrlMean",
                    weight=1.0
                ).xml,
                ScaleOperator(
                    id="ucrlSDScaleOperator",
                    parameter="@ucrlSD",
                    weight=3.0
                ).xml,
                IntegerRandomWalkOperator(
                    id="ucrlCategoriesRandomWalk",
                    parameter="@ucrlRateCategories"
                ).xml,
                SwapOperator(
                    id="ucrlCategoriesSwap",
                    parameter="@ucrlRateCategories"
                ).xml,
                UniformOperator(
                    id="ucrlCategoriesUniform",
                    parameter="@ucrlRateCategories"
                ).xml
            ]
            return "\n".join(operators)

    @property
    def xml_updown_operator(self) -> str:
        if self.fixed:
            return ""
        else:
            return UpDownOperator(
                id="ucrlMeanUpDownOperator",
                up_parameter="@ucrlMean",
                down_parameter="@Tree"
            ).xml
