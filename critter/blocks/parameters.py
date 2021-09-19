from math import inf as infinity
from pydantic import BaseModel, validator
from pydantic.errors import PydanticValueError


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
        
        if self.lower == -infinity:
            lower = "-Infinity"
        else:
            lower = f"{self.lower}"
        if self.upper == infinity:
            upper = "Infinity"
        else:
            upper = f"{self.upper}"

        return f'<parameter id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'estimate="{str(self.estimate).lower()}" ' \
               f'lower="{lower}" ' \
               f'upper="{upper}" ' \
               f'name="{self.name}">{self.value}' \
               f'</parameter>'

    @validator('value')
    def validate_value_is_float(cls, v):
        try:
            for s in v.split(' '):
                float(s) 
        except ValueError:
            raise PydanticValueError('If parameter value is a string, its split components must be convertable to float')
        return v

    @validator('lower')
    def validate_lower_bound_is_not_positive_infinity(cls, v):
        if v == infinity:
            raise PydanticValueError("Lower parameter value should not be +infinity")
        return v

    @validator('upper')
    def validate_upper_bound_is_not_negative_infinity(cls, v):
        if v == -infinity:
            raise PydanticValueError("Upper parameter value should not be -infinity")
        return v

class RealParameter(Parameter):
    spec: str = "parameter.RealParameter"

