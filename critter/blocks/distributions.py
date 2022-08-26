""" Distribution models """

from critter.blocks.parameters import RealParameter
from critter.utils import get_uuid
from typing import List, Optional
from pydantic import BaseModel, PrivateAttr


class Distribution(BaseModel):
    _id: str = PrivateAttr()
    _params: List[RealParameter] = PrivateAttr(default=[])
    _attr_name: dict = PrivateAttr(
        default={
            'real_space': 'meanInRealSpace',
            'mode': 'mode',
            'sd_parameter': 'S'   # used in branchRateParameter LogNormal with @
        }
    )

    def __init__(self, **data):
        super().__init__(**data)
        self._id: str = f'Distribution.{get_uuid(short=False)}'

    def __str__(self):
        return self.xml

    @property
    def xml(self):
        _param_block = "".join([str(param) for param in self._params])
        return f'<{self.__class__.__name__} ' \
               f'id="{self._id}" ' \
               f'{self._get_distr_config()} ' \
               f'name="distr">' \
               f'{_param_block}' \
               f'</{self.__class__.__name__}>'

    def _get_distr_config(self) -> str:
        """ Get optional distribution configs from subclasses """
        return ' '.join([
            f'{self._attr_name[attr]}="{value if not isinstance(value, bool) else str(value).lower()}"'
            for attr, value in vars(self).items()
            if value is not None and attr in self._attr_name.keys()
        ])


class Uniform(Distribution):
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id: str = f"Uniform.{get_uuid(short=False)}"


class Exponential(Distribution):
    mean: float

    _mean_id: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)

        self._id: str = f"Exponential.{get_uuid(short=False)}"
        self._mean_id = f'RealParameter.{get_uuid(short=False)}'

        self._params: List[RealParameter] = [
            RealParameter(
                id=self._mean_id,
                name="mean",
                value=self.mean,
                estimate=False
            )
        ]


class LogNormal(Distribution):
    mean: Optional[float] = ...  # required but can take None
    sd: Optional[float]  = ...

    sd_parameter: Optional[str] # used in branchRateModel LogNormal with @
    real_space: Optional[bool] = False

    _mean_id: str = PrivateAttr()
    _sd_id: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._id: str = f"LogNormal.{get_uuid(short=False)}"
        self._mean_id = f'RealParameter.{get_uuid(short=False)}'
        self._sd_id = f'RealParameter.{get_uuid(short=False)}'       

        if self.mean is not None:
            self._params.append(
                RealParameter(
                    id=self._mean_id,
                    name="M",
                    value=self.mean,
                    estimate=False
                )
            )
        if self.sd is not None:  # SD in branchRateParameter part of main parameters
            self._params.append(
                RealParameter(
                    id=self._sd_id,
                    name="S",
                    value=self.sd,
                    estimate=False
                )
            )


class Beta(Distribution):
    alpha: float
    beta: float

    _alpha_id: str = PrivateAttr()
    _beta_id: str = PrivateAttr()
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id: str = f"Beta.{get_uuid(short=False)}"
        self._alpha_id = f'RealParameter.{get_uuid(short=False)}'
        self._beta_id = f'RealParameter.{get_uuid(short=False)}'

        self._params: List[RealParameter] = [
            RealParameter(
                id=self._alpha_id,
                name="alpha",
                value=self.alpha,
                estimate=False
            ),
            RealParameter(
                id=self._beta_id,
                name="beta",
                value=self.beta,
                estimate=False
            )
        ]


class Gamma(Distribution):
    alpha: float
    beta: float
    mode: Optional[str] = "ShapeMean"
    
    _alpha_id: str = PrivateAttr()
    _beta_id: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)

        self._id: str = f"Gamma.{get_uuid(short=False)}"
        self._alpha_id = f'RealParameter.{get_uuid(short=False)}'
        self._beta_id = f'RealParameter.{get_uuid(short=False)}'

        self._params: List[RealParameter] = [
            RealParameter(
                id=self._alpha_id,
                name="alpha",
                value=self.alpha,
                estimate=False
            ),
            RealParameter(
                id=self._beta_id,
                name="beta",
                value=self.beta,
                estimate=False
            )
        ]


