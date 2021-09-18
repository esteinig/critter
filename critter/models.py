from typing import Tuple
from pathlib import Path
from critter.critter import Critter
from critter.blocks.clocks import Clock
from critter.blocks.priors import OriginPrior
from critter.blocks.priors import ReproductiveNumberPrior
from critter.blocks.priors import BecomeUninfectiousRatePrior
from critter.blocks.priors import SamplingProportionPrior


class BirthDeathSkylineSerial(Critter):

    def write(self, xml: Path):
        with xml.open('w') as xml_out:
            xml_out.write(self.xml)

    def configure(
        self,
        clock: Clock,
        origin: OriginPrior,
        sampling_proportion: SamplingProportionPrior,
        reproductive_number: ReproductiveNumberPrior,
        become_uninfectious_rate: BecomeUninfectiousRatePrior
    ) -> str:

        template = self.load_template(name='bdss.xml')

        xml_slice_functions, xml_slice_rate_change_times, xml_slice_loggers = \
            self.get_slice_xmls(
                priors=(reproductive_number, become_uninfectious_rate, sampling_proportion)
            )

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
            slice_functions=xml_slice_functions,
            slice_rates=xml_slice_rate_change_times,
            slice_loggers=xml_slice_loggers
        )

        return self.xml

    @staticmethod
    def get_slice_xmls(
        priors: Tuple[ReproductiveNumberPrior, BecomeUninfectiousRatePrior, SamplingProportionPrior]
    ) -> Tuple[str, str, str]:

        reverse_time_array = \
            '<reverseTimeArrays spec="beast.core.parameter.BooleanParameter" ' \
            'value="{0} {1} {2} false false"/>\n'.format(
                str(priors[0].sliced).lower(),
                str(priors[1].sliced).lower(),
                str(priors[2].sliced).lower()
            )
        slice_function_xml, slice_rate_change_times_xml, slice_logger_xml = "", "", ""
        for p in priors:
            slice_function_xml += p.xml_slice_function
            slice_rate_change_times_xml += p.xml_slice_rate_change_times
            slice_logger_xml += p.xml_slice_logger

        # if no priors are sliced, empty slice functions,
        # rates or loggers are returned, do not configure
        # the reverse time array in this case either
        if len(slice_function_xml) == 0:
            reverse_time_array = ""

        slice_rate_change_times_xml += reverse_time_array
        return slice_function_xml, slice_rate_change_times_xml, slice_logger_xml

