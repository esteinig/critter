from critter.blocks.misc import BranchRateModel
from critter.blocks.operators import Operator
from critter.blocks.priors import Prior
from pydantic import BaseModel, ValidationError, validator
from critter.utils import get_uuid
from typing import List
from critter.blocks.priors import Rate, UCED, UCLDMean, UCLDSD


class Clock(BaseModel):
    """ Base class for clock models """
    id: str = f'Clock.{get_uuid(short=True)}'

    priors: List[Prior]
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
        return "\n".join([p.xml_prior for p in self.priors])

    @property
    def xml_param(self):
        return "\n".join([p.xml_param for p in self.priors])

    @property
    def xml_logger(self):
        return "\n".join([p.xml_logger for p in self.priors])

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

    @validator('priors')
    def priors_must_be_clock_priors(self, field):
        for prior in field:
            if not isinstance(prior, (Rate, UCED, UCLDMean, UCLDSD)):
                raise ValidationError(
                    "Clocks must be populated with valid clock prior instances of: Rate, UCED, UCLDMean or UCLDSD"
                )
        return field


class Strict(Clock):

    @property
    def xml_branch_rate_model(self) -> str:
        return f'<branchRateModel id="StrictClock.c:snp" spec="beast.evolution.branchratemodel.StrictClockModel" clock.rate="@clockRate.c:snp"/>'

    def xml_scale_operator(self):
        if self.fixed:
            return ""
        else:
            return f'<operator id="StrictClockRateScaler.c:snp" spec="ScaleOperator" parameter="@clockRate.c:snp" scaleFactor="0.5" weight="3.0"/>'

    def xml_updown_operator(self) -> str:
        if self.fixed:
            return ""
        else:
            return textwrap.dedent(f"""
                <operator id="strictClockUpDownOperator.c:snp" spec="UpDownOperator" scaleFactor="0.75" weight="3.0">
                    <up idref="clockRate.c:snp"/>
                    <down idref="Tree.t:snp"/>
                </operator>
            """)


class RelaxedExponential(Clock):
    state_node = f'<stateNode id="expRateCategories.c:snp" spec="parameter.IntegerParameter" dimension="718">1</stateNode>'

    def get_branch_rate_xml(self) -> str:
        return textwrap.dedent(f""" 
            <branchRateModel id="ExponentialRelaxedClock.c:snp" spec="beast.evolution.branchratemodel.UCRelaxedClockModel" clock.rate="@ucedMean.c:snp" rateCategories="@expRateCategories.c:snp" tree="@Tree.t:snp">
                <Exponential id="Exponential.c:snp" name="distr">
                    <parameter id="UCExpLambda.c:snp" spec="parameter.RealParameter" name="mean">1.0</parameter>
                </Exponential>
            </branchRateModel>
        """)

    def get_scale_operator_xml(self):
        if self.fixed:
            return ''
        else:
            return textwrap.dedent(f""" 
                <operator id="ucedMeanScaler.c:snp" spec="ScaleOperator" parameter="@ucedMean.c:snp" scaleFactor="0.5" weight="1.0"/>
                <operator id="ExpCategoriesRandomWalk.c:snp" spec="IntRandomWalkOperator" parameter="@expRateCategories.c:snp" weight="10.0" windowSize="1"/>
                <operator id="ExpCategoriesSwapOperator.c:snp" spec="SwapOperator" intparameter="@expRateCategories.c:snp" weight="10.0"/>
                <operator id="ExpCategoriesUniform.c:snp" spec="UniformOperator" parameter="@expRateCategories.c:snp" weight="10.0"/>
            """)

    def get_updown_operator_xml(self):
        if self.fixed:
            return ''
        else:
            return textwrap.dedent(f"""
                <operator id="relaxedUpDownOperatorExp.c:snp" spec="UpDownOperator" scaleFactor="0.75" weight="3.0">
                    <up idref="ucedMean.c:snp"/>
                    <down idref="Tree.t:snp"/>
                </operator>
            """)


class RelaxedLogNormal(Clock):
    state_node = f'<stateNode id="rateCategories.c:snp" spec="parameter.IntegerParameter" dimension="718">1</stateNode>'

    def get_branch_rate_xml(self) -> str:
        return textwrap.dedent(f""" 
            <branchRateModel id="RelaxedClock.c:snp" spec="beast.evolution.branchratemodel.UCRelaxedClockModel" clock.rate="@ucldMean.c:snp" rateCategories="@rateCategories.c:snp" tree="@Tree.t:snp">
                <LogNormal id="LogNormalDistributionModel.c:snp" S="@ucldSD" meanInRealSpace="true" name="distr">
                    <parameter id="RealParameter.{uuid.uuid4()}" spec="parameter.RealParameter" estimate="false" lower="0.0" name="M" upper="1.0">1.0</parameter>
                </LogNormal>
            </branchRateModel>
        """)

    def get_scale_operator_xml(self):
        if self.fixed:
            return ""
        else:
            return textwrap.dedent(f""" 
                <operator id="ucldMeanScaler.c:snp" spec="ScaleOperator" parameter="@ucldMeanRate" scaleFactor="0.5" weight="1.0"/>
                <operator id="ucldStdevScaler.c:snp" spec="ScaleOperator" parameter="@ucldSD" scaleFactor="0.5" weight="3.0"/>
                <operator id="CategoriesRandomWalk.c:snp" spec="IntRandomWalkOperator" parameter="@rateCategories" weight="10.0" windowSize="1"/>
                <operator id="CategoriesSwapOperator.c:snp" spec="SwapOperator" intparameter="@rateCategories" weight="10.0"/>
                <operator id="CategoriesUniform.c:snp" spec="UniformOperator" parameter="@rateCategories" weight="10.0"/>
            """)

    def get_updown_operator_xml(self):
        if self.fixed:
            return ""
        else:
            return textwrap.dedent(f"""
                <operator id="relaxedUpDownOperator.c:snp" spec="UpDownOperator" scaleFactor="0.75" weight="3.0">
                    <up idref="ucldMean.c:snp"/>
                    <down idref="Tree.t:snp"/>
                </operator>
            """)