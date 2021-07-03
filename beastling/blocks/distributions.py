""" Distribution models """

from beastling.blocks.base import Distribution
from beastling.blocks.base import RealParameter
from beastling.utils import get_uuid
from typing import List


class Uniform(Distribution):
    id: str = f"Uniform.{get_uuid(short=True)}"


class Exponential(Distribution):
    id: str = f"Exponential.{get_uuid(short=True)}"

    mean: float = 1.0

    def __init__(self, mean_id: str = f'RealParameter.{get_uuid(short=True)}'):
        super().__init__()
        _params: List[RealParameter] = [
            RealParameter(id=mean_id, name="mean", value=self.mean)
        ]


class Beta(Distribution):
    id: str = f"Beta.{get_uuid(short=True)}"

    alpha: float = 1.0
    beta: float = 1.25

    def __init__(
        self, alpha_id: str = f'RealParameter.{get_uuid(short=True)}',
        beta_id: str = f'RealParameter.{get_uuid(short=True)}'
    ):
        super().__init__()
        _params: List[RealParameter] = [
            RealParameter(id=alpha_id, name="alpha", value=self.alpha),
            RealParameter(id=beta_id, name="beta", value=self.beta)
        ]


class Gamma(Distribution):
    id: str = f"Gamma.{get_uuid(short=True)}"

    alpha: float = 1.0
    beta: float = 1.25
    mode: str = "ShapeMean"

    def __init__(
        self, alpha_id: str = f'RealParameter.{get_uuid(short=True)}',
        beta_id: str = f'RealParameter.{get_uuid(short=True)}'
    ):
        super().__init__()
        _params: List[RealParameter] = [
            RealParameter(id=alpha_id, name="alpha", value=self.alpha),
            RealParameter(id=beta_id, name="beta", value=self.beta)
        ]


class LogNormal(Distribution):
    id: str = f"LogNormal.{get_uuid(short=True)}"
    
    mean: float = 1.0
    sd: float = 1.25
    real_space: bool = False

    def __init__(
        self, mean_id: str = f'RealParameter.{get_uuid(short=True)}',
        sd_id: str = f'RealParameter.{get_uuid(short=True)}'
    ):
        super().__init__()
        _params: List[RealParameter] = [
            RealParameter(id=mean_id, name="mean", value=self.mean),
            RealParameter(id=sd_id, name="sd", value=self.sd)
        ]
