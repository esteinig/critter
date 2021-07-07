from pydantic import BaseModel


class Operator(BaseModel):
    """ <operator/> """

    id: str = "ucedMeanScaler"
    spec: str = "ScaleOperator"
    parameter: str = "@ucedMean"
    scaleFactor: float = 0.5
    weight: float = 1.0

    # optional sub model pythonic attributes -> original name
    _attr_name = {
        'scale_factor': 'scaleFactor',
        'mode': 'mode'
    }

    def __str__(self):
        return self.xml

    @property
    def xml(self):
        return "<operator></operator>"