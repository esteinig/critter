""" Distribution models """

from critter.blocks.base import Distribution
from critter.blocks.base import RealParameter
from critter.utils import get_uuid
from typing import List


# PATTERN: DISTRIBUTION WITH PARAMS
class LogNormal(Distribution):
    # Distribution specific configs (passed on to Distribution)
    id: str = f"LogNormal.{get_uuid(short=True)}"
    real_space: bool = False

    # RealParameter specific configs (init on class init)
    def __init__(
        self,
        mean: float = 2.0,
        sd: float = 1.5,
        mean_id: str = f'RealParameter.{get_uuid(short=True)}',
        sd_id: str = f'RealParameter.{get_uuid(short=True)}',
        **distr_config  # passing on distribution config fields
    ):
        super().__init__(**distr_config)
        # Define the parameter attributes for testing access
        self.mean = mean
        self.sd = sd
        self.mean_id = mean_id
        self.sd_id = sd_id
        # RealParameters have to be instantiated within __init__ for model access
        self.params: List[RealParameter] = [
            RealParameter(id=mean_id, name="mean", value=mean),
            RealParameter(id=sd_id, name="sd", value=sd),
        ]


# PATTERN: DISTRIBUTION WITHOUT PARAMS
class Uniform(Distribution):
    id: str = f"Uniform.{get_uuid(short=True)}"
    params: List[RealParameter] = list()


class Exponential(Distribution):
    id: str = f"Exponential.{get_uuid(short=True)}"

    def __init__(self, mean: float = 1.0, mean_id: str = f'RealParameter.{get_uuid(short=True)}', **distr_config):
        super().__init__(**distr_config)
        self.mean = mean
        self.mean_id = mean_id
        self.params: List[RealParameter] = [
            RealParameter(id=mean_id, name="mean", value=mean)
        ]


class Beta(Distribution):
    id: str = f"Beta.{get_uuid(short=True)}"

    def __init__(
        self,
        alpha: float = 1.25,
        beta: float = 1.0,
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
            RealParameter(id=alpha_id, name="alpha", value=alpha),
            RealParameter(id=beta_id, name="beta", value=beta),
        ]


class Gamma(Distribution):
    id: str = f"Gamma.{get_uuid(short=True)}"
    mode: str = "ShapeMean"

    def __init__(
        self,
        alpha: float = 1.0,
        beta: float = 1.25,
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
            RealParameter(id=alpha_id, name="alpha", value=alpha),
            RealParameter(id=beta_id, name="beta", value=beta),
        ]


