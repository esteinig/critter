from typing import Tuple, List
from pathlib import Path
from critter.blocks import substitutions
from critter.critter import Critter
from critter.blocks.clocks import Clock
from critter.blocks.substitutions import SubstitutionModel
from critter.blocks.priors import OriginPrior
from critter.blocks.priors import ReproductiveNumberPrior
from critter.blocks.priors import BecomeUninfectiousRatePrior
from critter.blocks.priors import SamplingProportionPrior


class DynamicModel:

    def configure(
        configs: List[str]
    ):
        pass


class BirthDeathSkylineSerial:

    def __init__(
        self,
        critter: Critter,
        substitution: SubstitutionModel,
        clock: Clock,
        origin: OriginPrior,
        sampling_proportion: SamplingProportionPrior,
        reproductive_number: ReproductiveNumberPrior,
        become_uninfectious_rate: BecomeUninfectiousRatePrior
    ):
        self.critter = critter
        self.substitution = substitution
        self.clock = clock
        self.origin = origin
        self.sampling_proportion = sampling_proportion
        self.reproductive_number = reproductive_number
        self.become_uninfectious_rate = become_uninfectious_rate

        self.template = critter.load_template(name='bdss.xml')

    def render(self, xml_file: Path):

        xml_slice_functions, xml_slice_rate_change_times, xml_slice_loggers = \
            self.get_slice_xmls(
                priors=(self.reproductive_number, self.become_uninfectious_rate, self.sampling_proportion)
            )

        xml = self.template.render(
            # Run config
            data_xml=self.critter.xml_alignment,
            date_xml=self.critter.xml_dates,
            mcmc_xml=self.critter.xml_run,
            tree_log=self.critter.tree_log,
            tree_every=self.critter.sample_every,
            posterior_log=self.critter.posterior_log,
            posterior_every=self.critter.sample_every,
            ambiguities=self.critter.xml_ambiguities,
            # Model priors
            origin_param=self.origin.xml_param,
            origin_prior=self.origin.xml_prior,
            reproductive_number_param=self.reproductive_number.xml_param,
            reproductive_number_prior=self.reproductive_number.xml_prior,
            sampling_proportion_param=self.sampling_proportion.xml_param,
            sampling_proportion_prior=self.sampling_proportion.xml_prior,
            become_uninfectious_param=self.become_uninfectious_rate.xml_param,
            become_uninfectious_prior=self.become_uninfectious_rate.xml_prior,
            # Clock model
            clock_param=self.clock.xml_param,
            clock_prior=self.clock.xml_prior,
            clock_state_node=self.clock.xml_state_node,
            clock_branch_rate=self.clock.xml_branch_rate_model,
            clock_scale_operator=self.clock.xml_scale_operator,
            clock_updown_operator=self.clock.xml_updown_operator,
            clock_logger=self.clock.xml_logger,
            # Substitution model
            substitution_param=self.substitution.xml_param,
            substitution_prior=self.substitution.xml_prior,
            substitution_model=self.substitution.xml_model,
            substitution_operator=self.substitution.xml_operator,
            substitution_logger=self.substitution.xml_logger,
            # Slices
            slice_functions=xml_slice_functions,
            slice_rates=xml_slice_rate_change_times,
            slice_loggers=xml_slice_loggers
        )

        with xml_file.open('w') as xml_out:
            xml_out.write(xml)

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

