from pydantic import BaseModel, ValidationError, root_validator, validator
from critter.blocks.distributions import Gamma, LogNormal, Uniform
from critter.blocks.parameters import RealParameter
from critter.blocks.operators import FrequenciesExchanger, ScaleOperator
from critter.blocks.priors import Prior
from critter.errors import CritterError
from math import inf as infinity
from typing import List


class SubstitutionModel(BaseModel):
    """ <substModel/>"""
    id: str
    spec: str

    @property
    def xml(self) -> str:
        return None  # base model class

    @property
    def xml_model(self) -> str:
        return self.xml

    @property
    def xml_prior(self) -> str:
        return "\n".join([prior.xml for prior in self.priors])

    @property
    def xml_param(self) -> str:
        return "\n".join([param.xml for param in self.params])

    @property
    def xml_operator(self) -> str:
        return "\n".join([operator.xml for operator in self.operators])

    @property
    def xml_logger(self) -> str:
        return None


class HKY(SubstitutionModel):
    id = "HKY"
    spec = "HKY"

    priors = [
        Prior(id="kappa", distribution=[LogNormal(mean=1.0, sd=1.25)], initial=[2.0])
    ]

    params = [
        RealParameter(id="kappa", name="stateNode", lower=0, value="2.0")
    ]

    operators = [
        ScaleOperator(id="kappaScaler", parameter="@kappa", scale_factor=0.5, weight=0.1)
    ]

    @property
    def xml(self) -> str:
        return f'<substModel ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'kappa="@kappa" >' \
               f'<frequencies id="empiricalFreqs" spec="Frequencies" data="@Alignment"/>' \
               f'</substModel>'
    
    @property
    def xml_logger(self) -> str:
        return """<log idref="kappa"/>"""


class GTR(SubstitutionModel):
    id = "GTR"
    spec = "GTR"

    # Fixed priors for now, generally not configured
    # but may change in future versions
    priors = [
        Prior(id="frequencyParameter", distribution=[Uniform()], initial=[0.25]),
        Prior(id="rateAC", distribution=[Gamma(alpha=0.05, beta=10.0)], initial=[1.0]),
        Prior(id="rateAG", distribution=[Gamma(alpha=0.05, beta=20.0)], initial=[1.0]),
        Prior(id="rateAT", distribution=[Gamma(alpha=0.05, beta=10.0)], initial=[1.0]),
        Prior(id="rateCG", distribution=[Gamma(alpha=0.05, beta=10.0)], initial=[1.0]),
        Prior(id="rateGT", distribution=[Gamma(alpha=0.05, beta=10.0)], initial=[1.0])
    ]

    params = [
        RealParameter(id="frequencyParameter", name="stateNode", dimension=4, lower=0, upper=1, value="0.25"),
        RealParameter(id="rateAC", name="stateNode", lower=0, value="1.0"),
        RealParameter(id="rateAG", name="stateNode", lower=0, value="1.0"),
        RealParameter(id="rateAT", name="stateNode", lower=0, value="1.0"),
        RealParameter(id="rateCG", name="stateNode", lower=0, value="1.0"),
        RealParameter(id="rateGT", name="stateNode", lower=0, value="1.0")
    ]

    operators = [
        FrequenciesExchanger(id="FrequenciesExchanger", parameter="@frequencyParameter"),
        ScaleOperator(id="rateScalerAC", parameter="@rateAC", scale_factor=0.5, weight=0.1),
        ScaleOperator(id="rateScalerAG", parameter="@rateAG", scale_factor=0.5, weight=0.1),
        ScaleOperator(id="rateScalerAT", parameter="@rateAT", scale_factor=0.5, weight=0.1),
        ScaleOperator(id="rateScalerCG", parameter="@rateCG", scale_factor=0.5, weight=0.1),
        ScaleOperator(id="rateScalerGT", parameter="@rateGT", scale_factor=0.5, weight=0.1)
    ]

    @property
    def xml(self) -> str:
        return f'<substModel ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'rateAC="@rateAC" ' \
               f'rateAG="@rateAG" ' \
               f'rateAT="@rateAT" ' \
               f'rateCG="@rateCG" ' \
               f'rateGT="@rateGT" >' \
               f'{RealParameter(id="rateCT", name="rateCT", estimate=False, lower=0, value="1.0").xml}' \
               f'<frequencies id="estimatedFreqs" spec="Frequencies" frequencies="@frequencyParameter"/>' \
               f'</substModel>'

    @property
    def xml_logger(self) -> str:
        return """
        <log idref="frequencyParameter"/>
        <log idref="rateAC"/>
        <log idref="rateAG"/>
        <log idref="rateAT"/>
        <log idref="rateCG"/>
        <log idref="rateGT"/>
        """

