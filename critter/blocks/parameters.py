from math import inf as infinity
from pydantic import BaseModel, validator
from pydantic.error_wrappers import ValidationError


class Parameter(BaseModel):
    """ <parameter/> """
    id: str 
    name: str
    value: str  # allows multiple values for sliced configs [1.0 2.0]
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

    @validator('value')
    def validate_value_is_float(cls, v):
        try:
            for s in v.split(' '):
                float(s) 
        except ValueError:
            raise ValidationError('If parameter value is a string, its split components must be convertable to float')
        return v

class RealParameter(Parameter):
    spec: str = "parameter.RealParameter"

