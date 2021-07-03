""" Base blocks used to build higher level blocks """

from math import inf as infinity
from pydantic import BaseModel, validator
from beastling.utils import get_uuid


class RealParameter(BaseModel):
    """ <parameter/> """
    id: str = get_uuid()
    name: str
    value: float
    lower: float = -infinity
    upper: float = +infinity
    dimension: int = 1
    estimate: bool = False

    def __str__(self):

        return f'<parameter id="RealParameter.{self.id}" ' \
               f'spec="parameter.RealParameter" ' \
               f'estimate="{str(self.estimate).lower()}" ' \
               f'lower="{str(self.lower)}" ' \
               f'upper="{str(self.upper)}" ' \
               f'name="{self.name}">{self.value}</parameter>'


class Operator(BaseModel):
    """ <operator/> """
    pass