""" Base blocks mirroring BEAST 2.5 """

from math import inf as infinity
from pydantic import BaseModel
from typing import List


class RealParameter(BaseModel):
    """ <parameter/> """
    id: str
    name: str
    value: float
    lower: float = -infinity
    upper: float = +infinity
    dimension: int = 1
    estimate: bool = False

    def __str__(self):
        return f'<parameter id="{self.id}" ' \
               f'spec="parameter.RealParameter" ' \
               f'estimate="{str(self.estimate).lower()}" ' \
               f'lower="{str(self.lower)}" ' \
               f'upper="{str(self.upper)}" ' \
               f'name="{self.name}">{self.value}' \
               f'</parameter>'


class Distribution(BaseModel):
    """ Distribution base class """
    id: str
    # parameters defined in subclasses as RealParameters
    # this let's users config the parameter block id
    params: List[RealParameter] = list()
    # sub model attributes match original name
    _attr_name = {
        'real_space': 'meanInRealSpace',
        'mode': 'mode'
    }

    def __str__(self):

        _param_block = "".join([str(param) for param in self.params])
        return f'<{self.__class__.__name__} id="{self.id}" ' \
               f'{self._get_distr_config()} name="distr">' \
               f'{_param_block}</{self.__class__.__name__}>'

    def _get_distr_config(self) -> str:
        """ Get optional distribution configs from subclasses """
        return ' '.join([
            f'{self._attr_name[attr] if attr in self._attr_name.keys() else attr}="{value}"'
            for attr, value in vars(self).items()
            if attr not in ('id', 'name', 'params')
        ])


class Operator(BaseModel):
    """ <operator/> """
    pass