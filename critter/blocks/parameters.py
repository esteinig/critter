
from math import inf as infinity
from pydantic import BaseModel


class Parameter(BaseModel):
    """ <parameter/> """
    id: str
    name: str
    value: float
    lower: float = -infinity
    upper: float = +infinity
    dimension: int = 1
    estimate: bool = False
    spec: str = "parameter.RealParameter"

    def __str__(self) -> str:
        return self.xml

    @property
    def xml(self) -> str:
        return f'<parameter id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'estimate="{str(self.estimate).lower()}" ' \
               f'lower="{str(self.lower)}" ' \
               f'upper="{str(self.upper)}" ' \
               f'name="{self.name}">{self.value}' \
               f'</parameter>'


class RealParameter(Parameter):
    spec: str = "parameter.RealParameter"

