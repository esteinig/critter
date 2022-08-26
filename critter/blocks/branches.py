from pydantic import BaseModel
from critter.blocks.distributions import Distribution
from critter.blocks.distributions import Exponential
from critter.blocks.distributions import LogNormal
from critter.blocks.parameters import RealParameter
from critter.utils import get_uuid


class BranchRateModel(BaseModel):
    """ <branchRateModel/>"""

    id: str
    spec: str
    parameter: str  # clock rate parameter targeted

    # Relaxed clock model parameters when distribution
    distribution: Distribution = None
    rate_categories_parameter: str = ""
    tree_parameter: str = ""

    def __str__(self):
        return self.xml

    @property
    def xml(self):
        return f'<branchRateModel ' \
               f'id="{self.id}" ' \
               f'spec="{self.spec}" ' \
               f'clock.rate="{self.parameter}" ' \
               f'{self.get_relaxed_model_parameters()}>' \
               f'{"" if self.distribution is None else self.distribution}' \
               f'</branchRateModel>'

    def get_relaxed_model_parameters(self):

        if self.distribution is not None:
            return f'rateCategories="{self.rate_categories_parameter}" ' \
                   f'tree="{self.tree_parameter}"'
        else:
            return ''


class StrictBranchRateModel(BranchRateModel):
    spec: str = "beast.evolution.branchratemodel.StrictClockModel"


class UCREBranchRateModel(BranchRateModel):
    spec: str = "beast.evolution.branchratemodel.UCRelaxedClockModel"
    distribution: Distribution = Exponential(mean=1.0)


class UCRLBranchRateModel(BranchRateModel):
    spec: str = "beast.evolution.branchratemodel.UCRelaxedClockModel"
    # This is a bit weird, because the SD parameter is contained in the distribution
    # main parameters, it is currently the only instance where this happens, also
    # needed to bound the lower and upper values (as per template) - this is currently
    # not accessible from higher levels
    distribution: Distribution = LogNormal(
        mean=1.0,
        sd=None,
        sd_parameter="@ucrlSD",
        real_space=True,
        params=[
            RealParameter(
                id=f"RealParameter.{get_uuid(short=False)}",
                name="M",
                value=1.0,
                lower=0.,
                upper=1.0
            )
        ]
    )

