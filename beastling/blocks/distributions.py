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
    mean_id: str = f'RealParameter.{get_uuid(short=True)}'

    params: List[RealParameter] = [
        RealParameter(id=mean_id, name="mean", value=mean)
    ]


class Beta(Distribution):
    id: str = f"Beta.{get_uuid(short=True)}"

    alpha: float = 1.25
    beta: float = 1.0
    alpha_id: str = f'RealParameter.{get_uuid(short=True)}'
    beta_id: str = f'RealParameter.{get_uuid(short=True)}'

    params: List[RealParameter] = [
        RealParameter(id=alpha_id, name="alpha", value=alpha),
        RealParameter(id=beta_id, name="beta", value=beta),
    ]


class Gamma(Distribution):
    id: str = f"Gamma.{get_uuid(short=True)}"

    alpha: float = 1.0
    beta: float = 1.25
    mode: str = "ShapeMean"
    alpha_id: str = f'RealParameter.{get_uuid(short=True)}'
    beta_id: str = f'RealParameter.{get_uuid(short=True)}'

    params: List[RealParameter] = [
        RealParameter(id=alpha_id, name="alpha", value=alpha),
        RealParameter(id=beta_id, name="beta", value=beta),
    ]


class LogNormal(Distribution):
    id: str = f"LogNormal.{get_uuid(short=True)}"

    mean: float = 1.0
    sd: float = 1.25
    real_space: bool = False
    mean_id: str = f'RealParameter.{get_uuid(short=True)}'
    sd_id: str = f'RealParameter.{get_uuid(short=True)}'

    params: List[RealParameter] = [
        RealParameter(id=mean_id, name="mean", value=mean),
        RealParameter(id=sd_id, name="sd", value=sd),
    ]