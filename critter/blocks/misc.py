from pydantic import BaseModel


class BranchRateModel(BaseModel):
    """ <branchRateModel/>"""

    def __str__(self):
        return self.xml

    @property
    def xml(self):
        return "<branchRateModel></branchRateModel>"