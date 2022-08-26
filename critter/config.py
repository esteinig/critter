
# Defines the JSON schema to configure models outside
# of the API through JSON or YAML template files and
# import configurations with validation

# Should merge into combined block / config models in the future

import yaml
import json
from pathlib import Path
from enum import Enum
from typing import List, Optional, Dict
from critter.errors import CritterError
from pydantic import BaseModel, ValidationError
from critter.critter import Critter
from critter.models import BirthDeathSkylineSerial
from critter.blocks.substitutions import SubstitutionModel, GTR, HKY
from critter.blocks.clocks import Clock, StrictClock, UCREClock, UCRLClock
from critter.blocks.priors import BecomeUninfectiousRatePrior, ClockRatePrior, OriginPrior, ReproductiveNumberPrior, SamplingProportionPrior, UCREPrior, UCRLMeanPrior, UCRLSDPrior, Prior
from critter.blocks.distributions import Distribution, Uniform, Exponential, LogNormal, Beta, Gamma

# Restricted choices


class ModelType(str, Enum):
    bdss = 'birth_death_skyline_serial'
    bdsc = 'birth_death_skyline_contemporary'


class SubstitutionModelType(str, Enum):
    hky = 'hky'
    gtr = 'gtr'


class ModelPriorType(str, Enum):
    origin = 'origin'
    reproductive_number = 'reproductive_number'
    sampling_proportion = 'sampling_proportion'
    become_uninfectious_rate = 'become_uninfectious_rate'


class ClockPriorType(str, Enum):
    strict = 'strict'
    ucre = 'ucre'
    ucrl_mean = 'ucrl_mean'
    ucrl_sd = 'ucrl_sd'


class DistributionType(str, Enum):
    uniform = 'uniform'
    exponential = 'exponential'
    lognormal = 'lognormal'
    beta = 'beta'
    gamma = 'gamma'


# Prior component configs

class DistributionConfig(BaseModel):
    type: DistributionType 
    mean: Optional[float]
    sd: Optional[float]
    alpha: Optional[float]
    beta: Optional[float]
    real_space: Optional[bool]


class ModelPriorConfig(BaseModel):
    type: ModelPriorType
    dimension: int
    lower: float
    upper: float
    initial: List[float]
    distribution: List[DistributionConfig]
    sliced: bool = False  
    intervals: List[float] = []


class ClockPriorConfig(BaseModel):
    type: ClockPriorType
    dimension: int
    lower: float
    upper: float
    initial: List[float]
    distribution: List[DistributionConfig]


# Model global config

class ModelInfo(BaseModel):
    name: str
    cite: str
    info: str


class ModelConfig(BaseModel):
    type: ModelType 
    substitution_model: SubstitutionModelType
    fixed_clock: bool


# Configured model

class CritterConfig(BaseModel):

    model_info: ModelInfo
    model_config: ModelConfig
    clock_priors: List[ClockPriorConfig]
    model_priors: List[ModelPriorConfig]

    def __str__(self) -> str:

        return f"""
        Critter configuration
        =====================

        Model type: {self.model_config.type} 
        Substitution model: {self.model_config.substitution_model}
        Fixed clock: {self.model_config.fixed_clock}
        
        """

    def get_model(self, critter: Critter):
        """ Model factory from configured model schema """

        clock_model = self.get_clock_model()
        substitution_model = self.get_substitution_model()
        model_priors = self.get_model_priors()

        print(str(self))
        print(self.__dict__)

        if self.model_config.type == ModelType.bdss:
            return BirthDeathSkylineSerial(
                critter=critter,
                clock=clock_model,
                substitution=substitution_model,
                origin=model_priors.get('origin'),
                reproductive_number=model_priors.get('reproductive_number'),
                sampling_proportion=model_priors.get('sampling_proportion'),
                become_uninfectious_rate=model_priors.get('become_uninfectious_rate')
            )
        else:
            raise ValueError(f'Could not infer model type from given model configuration: {self.model_config.type}')

    def get_substitution_model(self) -> SubstitutionModel:
        
        if self.model_config.substitution_model == SubstitutionModelType.gtr:
            return GTR()
        elif self.model_config.substitution_model == SubstitutionModelType.hky:
            return HKY()
        else:
            raise CritterError(f"Substitution model not supported: {self.model_config.substitution_model }")


    def get_clock_priors(self) -> List[Prior]:
        """ Clock prior factory from configured model schema """
        
        configured = []
        for clock_prior in self.clock_priors:
            clock_config = clock_prior.dict()
            prior_type = clock_config.pop('type')
            clock_distrs = clock_config.pop('distribution')
            distributions = self.get_distribution_models(
                distributions=clock_distrs
            )

            if prior_type == 'strict':
                configured.append(
                    ClockRatePrior(
                        **clock_config, 
                        distribution=distributions
                    )
                )
            elif prior_type == 'ucre':
                configured.append(
                    UCREPrior(
                        **clock_config,
                        distribution=distributions
                    )
                )
            elif prior_type == 'ucrl_mean':
                configured.append(
                    UCRLMeanPrior(
                        **clock_config,
                        distribution=distributions
                    )
                )
            elif prior_type == 'ucrl_sd':
                configured.append(
                    UCRLSDPrior(
                        **clock_config,
                        distribution=distributions
                    )
                )
            else:
                raise ValueError(f'Unknown clock prior type: {prior_type}')
        return configured

    def get_clock_model(self) -> Clock:
        """ Clock model factory from configured model schema """

        clock_priors = self.get_clock_priors()

        if len(clock_priors) == 1 and isinstance(clock_priors[0], ClockRatePrior):

            return StrictClock(
                fixed=self.model_config.fixed_clock,
                prior=clock_priors
            )
        elif len(clock_priors) == 1 and isinstance(clock_priors[0], UCREPrior):
            return UCREClock(
                fixed=self.model_config.fixed_clock,
                prior=clock_priors
            )
        elif len(clock_priors) == 2 and isinstance(clock_priors[0], UCRLMeanPrior) \
            and isinstance(clock_priors[1], UCRLSDPrior):
            return UCRLClock(
                fixed=self.model_config.fixed_clock,
                prior=clock_priors
            )
        else:
            raise ValueError('Clock model could not be inferred from configured priors')

    def get_model_priors(self) -> Dict[str, Prior]:
        """ Model prior factory from configured model schema """

        configured = {}
        for model_prior in self.model_priors:
            model_cfg = model_prior.dict()
            prior_type = model_cfg.pop('type')
            model_distrs = model_cfg.pop('distribution')
            distributions = self.get_distribution_models(
                distributions=model_distrs
            )

            if prior_type == 'origin':
                configured[prior_type] = \
                    OriginPrior(
                        **model_cfg,
                        distribution=distributions
                    )
            elif prior_type == 'reproductive_number':
                configured[prior_type] = \
                    ReproductiveNumberPrior(
                        **model_cfg,
                        distribution=distributions
                    )
            elif prior_type == 'sampling_proportion':
                configured[prior_type] = \
                    SamplingProportionPrior(
                        **model_cfg,
                        distribution=distributions
                    )
            elif prior_type == 'become_uninfectious_rate':
                configured[prior_type] = \
                    BecomeUninfectiousRatePrior(
                        **model_cfg,
                        distribution=distributions
                    )
            else:
                raise ValueError(f'Unknown model prior type: {prior_type}')
        return configured


    @staticmethod
    def get_distribution_models(
        distributions: List[DistributionConfig]
    ) -> List[Distribution]:
        """ Distribution model factory from configured model schema """
        distr_models = []
        for distr_cfg in distributions:
            distr_type = distr_cfg.pop('type')
            distr_clean = {
                k:v for k, v in distr_cfg.items() 
                if v is not None
            }

            if distr_type == 'uniform':
                distr_models.append(
                    Uniform(**distr_clean)
                )
            elif distr_type == 'exponential':
                distr_models.append(
                    Exponential(**distr_clean)
                )
            elif distr_type == 'lognormal':
                distr_models.append(
                    LogNormal(**distr_clean)
                )
            elif distr_type == 'beta':
                distr_models.append(
                    Beta(**distr_clean)
                )
            elif distr_type == 'gamma':
                distr_models.append(
                    Gamma(**distr_clean)
                )

        return distr_models


# YAML loader

def load_config(yaml_file: Path) -> CritterConfig:
    """ Load model configuration from YAML """
    with yaml_file.open() as yml:
        config = yaml.safe_load(yml)
    try:
        return CritterConfig.parse_obj(config)
    except ValidationError:
        raise


# Dynamic config of template