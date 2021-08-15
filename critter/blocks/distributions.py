""" Distribution models """

from pydantic import BaseModel, Extra
from critter.blocks.parameters import RealParameter
from critter.utils import get_uuid
from typing import List


class Distribution(BaseModel, extra=Extra.allow):
    """ Distribution base class """
    id: str = f'Distribution.{get_uuid(short=True)}'
    # parameters defined in subclasses as RealParameters
    # this let's users config the parameter block id
    params: List[RealParameter] = list()
    # optional sub model pythonic attributes -> original name
    _attr_name = {
        'real_space': 'meanInRealSpace',
        'mode': 'mode',
        'sd_parameter': 'S'   # used in branchRateParameter LogNormal with @
    }

    def __str__(self):
        return self.xml

    @property
    def xml(self):
        _param_block = "".join([str(param) for param in self.params])
        return f'<{self.__class__.__name__} ' \
               f'id="{self.id}" ' \
               f'{self._get_distr_config()} ' \
               f'name="distr">' \
               f'{_param_block}' \
               f'</{self.__class__.__name__}>'

    def _get_distr_config(self) -> str:
        """ Get optional distribution configs from subclasses """
        return ' '.join([
            f'{self._attr_name[attr]}="{value}"'
            for attr, value in vars(self).items()
            if attr in self._attr_name.keys() and attr is not None
        ])


# PATTERN: DISTRIBUTION WITH PARAMS
class LogNormal(Distribution):
    # Distribution specific configs (passed on to Distribution)
    id: str = f"LogNormal.{get_uuid(short=True)}"
    sd_parameter: str = None  # used in branchRateModel LogNormal with @
    real_space: bool = False

    # RealParameter specific configs (params init on distribution init)
    def __init__(
        self,
        mean: float = None,
        sd: float = None,
        mean_id: str = f'RealParameter.{get_uuid(short=True)}',
        sd_id: str = f'RealParameter.{get_uuid(short=True)}',
        **distr_config  # passing on distribution config fields
    ):
        super().__init__(**distr_config)
        # Define the parameter attributes here for external / testing access
        self.mean = mean
        self.sd = sd
        self.mean_id = mean_id
        self.sd_id = sd_id

        if self.mean is not None:
            self.params.append(
                RealParameter(
                    id=mean_id,
                    name="M",
                    value=mean
                )
            )
        if self.sd is not None:  # SD in branchRateParameter part of main parameters
            self.params.append(
                RealParameter(
                    id=sd_id,
                    name="S",
                    value=sd
                )
            )


# PATTERN: DISTRIBUTION WITHOUT PARAMS
class Uniform(Distribution):
    id: str = f"Uniform.{get_uuid(short=True)}"


class Exponential(Distribution):
    id: str = f"Exponential.{get_uuid(short=True)}"

    def __init__(
        self,
        mean: float,
        mean_id: str = f'RealParameter.{get_uuid(short=True)}',
        **distr_config
    ):
        super().__init__(**distr_config)
        self.mean = mean
        self.mean_id = mean_id
        self.params: List[RealParameter] = [
            RealParameter(
                id=mean_id,
                name="mean",
                value=mean
            )
        ]


class Beta(Distribution):
    id: str = f"Beta.{get_uuid(short=True)}"

    def __init__(
        self,
        alpha: float,
        beta: float,
        alpha_id: str = f'RealParameter.{get_uuid(short=True)}',
        beta_id: str = f'RealParameter.{get_uuid(short=True)}',
        **distr_config
    ):
        super().__init__(**distr_config)
        self.alpha = alpha
        self.beta = beta
        self.alpha_id = alpha_id
        self.beta_id = beta_id
        self.params: List[RealParameter] = [
            RealParameter(
                id=alpha_id,
                name="alpha",
                value=alpha
            ),
            RealParameter(
                id=beta_id,
                name="beta",
                value=beta
            ),
        ]


class Gamma(Distribution):
    id: str = f"Gamma.{get_uuid(short=True)}"
    mode: str = "ShapeMean"

    def __init__(
        self,
        alpha: float,
        beta: float,
        alpha_id: str = f'RealParameter.{get_uuid(short=True)}',
        beta_id: str = f'RealParameter.{get_uuid(short=True)}',
        **distr_config
    ):
        super().__init__(**distr_config)
        self.alpha = alpha
        self.beta = beta
        self.alpha_id = alpha_id
        self.beta_id = beta_id
        self.params: List[RealParameter] = [
            RealParameter(
                id=alpha_id,
                name="alpha",
                value=alpha
            ),
            RealParameter(
                id=beta_id,
                name="beta",
                value=beta
            ),
        ]


