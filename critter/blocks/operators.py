from pydantic import BaseModel


class Operator(BaseModel):
    """ <operator/> """
    id: str
    spec: str

    def __str__(self) -> str:
        return self.xml

    @property
    def xml(self) -> str:
        return f'<operator ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}"/>'


# Specific subclasses defined by "spec"
class ScaleOperator(Operator):
    spec: str = "ScaleOperator"

    parameter: str
    weight: float = 1.0
    scale_factor: float = 0.5

    @property
    def xml(self):
        return f'<operator ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'parameter="{self.parameter}" ' \
               f'weight="{self.weight}" ' \
               f'scaleFactor="{self.scale_factor}">' \
               f'</operator>'


class IntegerRandomWalkOperator(Operator):
    spec: str = "IntRandomWalkOperator"

    parameter: str
    weight: float = 10.0
    window_size: int = 1

    @property
    def xml(self):
        return f'<operator ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'parameter="{self.parameter}" ' \
               f'weight="{self.weight}" ' \
               f'windowSize="{self.window_size}">' \
               f'</operator>'


class SwapOperator(Operator):
    spec: str = "SwapOperator"

    parameter: str
    weight: float = 10.0

    @property
    def xml(self):
        return f'<operator ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'intparameter="{self.parameter}" ' \
               f'weight="{self.weight}">' \
               f'</operator>'


class UniformOperator(Operator):
    spec: str = "UniformOperator"

    parameter: str
    weight: float = 10.0

    @property
    def xml(self):
        return f'<operator ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'parameter="{self.parameter}" ' \
               f'weight="{self.weight}">' \
               f'</operator>'


class UpDownOperator(Operator):
    spec: str = "UpDownOperator"

    up_idref: str
    down_idref: str
    weight: float = 3.0
    scale_factor: float = 0.75

    @property
    def xml(self):
        return f'<operator ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'weight="{self.weight}" ' \
               f'scaleFactor="{self.scale_factor}">' \
               f'<up idref="{self.up_idref}" />' \
               f'<down idref="{self.down_idref}" />' \
               f'</operator>'


class FrequenciesExchanger(Operator):
    spec: str = "DeltaExchangeOperator"

    parameter: str
    weight: float = 0.1
    delta: float = 0.01

    @property
    def xml(self):
        return f'<operator ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'parameter="{self.spec}" ' \
               f'delta="{self.delta}" ' \
               f'weight="{self.weight}">' \
               f'</operator>'

