from pathlib import Path
from critter.critter import Critter
from critter.blocks.priors import OriginPrior
from critter.blocks.priors import ReproductiveNumberPrior
from critter.blocks.priors import BecomeUninfectiousRatePrior
from critter.blocks.priors import SamplingProportionPrior
from critter.blocks.clocks import Clock
from typing import List


class BirthDeathSkylineSerial(Critter):

    def configure(
        self,
        reproductive_number: ReproductiveNumberPrior,
        become_uninfectious_rate: BecomeUninfectiousRatePrior,
        sampling_proportion: SamplingProportionPrior,
        origin: OriginPrior,
        clock: Clock
    ):

        template = self.load_template(name='bdss.xml')

        xml_slice_functions, xml_slice_rate_change_times, xml_slice_loggers = \
            self.get_slice_xmls(priors=[reproductive_number, become_uninfectious_rate, sampling_proportion])

        self.xml = template.render(
            data_xml=self.xml_alignment,
            date_xml=self.xml_dates,
            mcmc_xml=self.xml_run,
            tree_log=self.tree_log,
            tree_every=self.sample_every,
            posterior_log=self.posterior_log,
            posterior_every=self.sample_every,
            origin_param=origin.xml_param,
            origin_prior=origin.xml_prior,
            reproductive_number_param=reproductive_number.xml_param,
            reproductive_number_prior=reproductive_number.xml_prior,
            sampling_proportion_param=sampling_proportion.xml_param,
            sampling_proportion_prior=sampling_proportion.xml_prior,
            become_uninfectious_param=become_uninfectious_rate.xml_param,
            become_uninfectious_prior=become_uninfectious_rate.xml_prior,
            clock_param=clock.xml_param,
            clock_prior=clock.xml_prior,
            clock_state_node=clock.xml_state_node,
            clock_branch_rate=clock.xml_branch_rate_model,
            clock_scale_operator=clock.xml_scale_operator,
            clock_updown_operator=clock.xml_updown_operator,
            clock_logger=clock.xml_logger,
            slice_functions=slice_function_xml,
            slice_rates=slice_rate_xml,
            slice_loggers=slice_logger_xml
        )

    @staticmethod
    def get_slice_xmls(
        priors: List[ReproductiveNumberPrior, BecomeUninfectiousRatePrior, SamplingProportionPrior]
    ) -> (str, str, str):

        reverse_time_array = \
            '<reverseTimeArrays spec="beast.core.parameter.BooleanParameter" ' \
            'value="{0} {1} {2} false false"/>'.format(
                str(priors[0].sliced).lower(),
                str(priors[1].sliced).lower(),
                str(priors[2].sliced).lower()
            )
        slice_function_xml, slice_rate_xml, slice_logger_xml = "", "", ""
        for p in priors:
            slice_function_xml += p.xml_slice_function
            slice_rate_xml += p.xml_slice_rate_change_times
            slice_logger_xml += p.xml_slice_logger
        # why is this in here...
        if len(slice_function_xml) == 0:
            reverse_time_array = ""
        slice_rate_xml += reverse_time_array
        return slice_function_xml, slice_rate_xml, slice_logger_xml

    @staticmethod
    def write(self, xml: Path):
        with xml.open() as xml_out:
            xml_out.write(self.xml)
