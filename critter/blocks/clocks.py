from critter.blocks.base import Clock


class Strict(Clock):
    def __init__(self, priors):
        Clock.__init__(self, priors=priors)

    @property
    def xml_branch_rate_model(self) -> str:
        return f'<branchRateModel id="StrictClock.c:snp" spec="beast.evolution.branchratemodel.StrictClockModel" clock.rate="@clockRate.c:snp"/>'

    def xml_scale_operator(self):
        if self.fixed:
            return ""
        else:
            return f'<operator id="StrictClockRateScaler.c:snp" spec="ScaleOperator" parameter="@clockRate.c:snp" scaleFactor="0.5" weight="3.0"/>'

    def xml_updown_operator(self) -> str:
        if self.fixed:
            return ""
        else:
            return textwrap.dedent(f"""
                <operator id="strictClockUpDownOperator.c:snp" spec="UpDownOperator" scaleFactor="0.75" weight="3.0">
                    <up idref="clockRate.c:snp"/>
                    <down idref="Tree.t:snp"/>
                </operator>
            """)


class RelaxedExponential(Clock):
    def __init__(self, priors):
        Clock.__init__(self, priors=priors)
        self.state_node = f'<stateNode id="expRateCategories.c:snp" spec="parameter.IntegerParameter" dimension="718">1</stateNode>'

    def get_branch_rate_xml(self) -> str:
        return textwrap.dedent(f""" 
            <branchRateModel id="ExponentialRelaxedClock.c:snp" spec="beast.evolution.branchratemodel.UCRelaxedClockModel" clock.rate="@ucedMean.c:snp" rateCategories="@expRateCategories.c:snp" tree="@Tree.t:snp">
                <Exponential id="Exponential.c:snp" name="distr">
                    <parameter id="UCExpLambda.c:snp" spec="parameter.RealParameter" name="mean">1.0</parameter>
                </Exponential>
            </branchRateModel>
        """)

    def get_scale_operator_xml(self):
        if self.fixed:
            return ''
        else:
            return textwrap.dedent(f""" 
                <operator id="ucedMeanScaler.c:snp" spec="ScaleOperator" parameter="@ucedMean.c:snp" scaleFactor="0.5" weight="1.0"/>
                <operator id="ExpCategoriesRandomWalk.c:snp" spec="IntRandomWalkOperator" parameter="@expRateCategories.c:snp" weight="10.0" windowSize="1"/>
                <operator id="ExpCategoriesSwapOperator.c:snp" spec="SwapOperator" intparameter="@expRateCategories.c:snp" weight="10.0"/>
                <operator id="ExpCategoriesUniform.c:snp" spec="UniformOperator" parameter="@expRateCategories.c:snp" weight="10.0"/>
            """)

    def get_updown_operator_xml(self):
        if self.fixed:
            return ''
        else:
            return textwrap.dedent(f"""
                <operator id="relaxedUpDownOperatorExp.c:snp" spec="UpDownOperator" scaleFactor="0.75" weight="3.0">
                    <up idref="ucedMean.c:snp"/>
                    <down idref="Tree.t:snp"/>
                </operator>
            """)


class RelaxedLogNormal(Clock):
    def __init__(self, priors):
        Clock.__init__(self, priors=priors)
        self.state_node = f'<stateNode id="rateCategories.c:snp" spec="parameter.IntegerParameter" dimension="718">1</stateNode>'

    def get_branch_rate_xml(self) -> str:
        return textwrap.dedent(f""" 
            <branchRateModel id="RelaxedClock.c:snp" spec="beast.evolution.branchratemodel.UCRelaxedClockModel" clock.rate="@ucldMean.c:snp" rateCategories="@rateCategories.c:snp" tree="@Tree.t:snp">
                <LogNormal id="LogNormalDistributionModel.c:snp" S="@ucldStdev.c:snp" meanInRealSpace="true" name="distr">
                    <parameter id="RealParameter.{uuid.uuid4()}" spec="parameter.RealParameter" estimate="false" lower="0.0" name="M" upper="1.0">1.0</parameter>
                </LogNormal>
            </branchRateModel>
        """)

    def get_scale_operator_xml(self):
        if self.fixed:
            return ""
        else:
            return textwrap.dedent(f""" 
                <operator id="ucldMeanScaler.c:snp" spec="ScaleOperator" parameter="@ucldMean.c:snp" scaleFactor="0.5" weight="1.0"/>
                <operator id="ucldStdevScaler.c:snp" spec="ScaleOperator" parameter="@ucldStdev.c:snp" scaleFactor="0.5" weight="3.0"/>
                <operator id="CategoriesRandomWalk.c:snp" spec="IntRandomWalkOperator" parameter="@rateCategories.c:snp" weight="10.0" windowSize="1"/>
                <operator id="CategoriesSwapOperator.c:snp" spec="SwapOperator" intparameter="@rateCategories.c:snp" weight="10.0"/>
                <operator id="CategoriesUniform.c:snp" spec="UniformOperator" parameter="@rateCategories.c:snp" weight="10.0"/>
            """)

    def get_updown_operator_xml(self):
        if self.fixed:
            return ""
        else:
            return textwrap.dedent(f"""
                <operator id="relaxedUpDownOperator.c:snp" spec="UpDownOperator" scaleFactor="0.75" weight="3.0">
                    <up idref="ucldMean.c:snp"/>
                    <down idref="Tree.t:snp"/>
                </operator>
            """)