from pydantic import BaseModel


class Operator(BaseModel):
    """ <operator/> """

    id: str
    spec: str  # e.g. "ScaleOperator"

    def __str__(self) -> str:
        return self.xml

    @property
    def xml(self) -> str:
        return f'<operator id="{self.id}" spec="{self.spec}"/>'


# Specific subclasses defined by "spec"
class ScaleOperator(Operator):
    spec: str = "ScaleOperator"
    parameter: str
    weight: float = 1.0
    scale_factor: float = 0.5

    @property
    def xml(self):
        return f'<operator id="{self.id}" spec="{self.spec}" parameter="{self.parameter}" ' \
               f'weight="{self.weight}" scaleFactor="{self.scale_factor}"></operator>'


class IntegerRandomWalkOperator(Operator):
    spec: str = "IntRandomWalkOperator"
    parameter: str
    weight: float = 10.0
    window_size: int = 1

    @property
    def xml(self):
        return f'<operator id="{self.id}" spec="{self.spec}" parameter="{self.parameter}" ' \
               f'weight="{self.weight}" windowSize="{self.window_size}"></operator>'


class SwapOperator(Operator):
    spec: str = "SwapOperator"
    parameter: str
    weight: float = 10.0

    @property
    def xml(self):
        return f'<operator id="{self.id}" spec="{self.spec}" intparameter="{self.parameter}" ' \
               f'weight="{self.weight}"></operator>'


class UniformOperator(Operator):
    spec: str = "UniformOperator"
    parameter: str
    weight: float = 10.0

    @property
    def xml(self):
        return f'<operator id="{self.id}" spec="{self.spec}" parameter="{self.parameter}" ' \
               f'weight="{self.weight}"></operator>'


class UpDownOperator(Operator):
    spec: str = "UpDownOperator"
    up_parameter: str
    down_parameter: str
    weight: float = 3.0
    scale_factor: float = 0.75

    @property
    def xml(self):
        return f'<operator id="{self.id}" spec="{self.spec}" weight="{self.weight}" scaleFactor="{self.scale_factor}">' \
               f'<up idref="{self.up_parameter}" />' \
               f'<down idref="{self.down_parameter}" />' \
               f'</operator>'
