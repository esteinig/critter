"""
Functions related to posterior diagnostics (aka Tracer)
"""

import pandas
from math import ceil
from pathlib import Path
from arviz.stats import hdi


class PosteriorDiagnostic:

    def __init__(self, log_file: Path, burnin: float = 0.1):
        
        self.log = log_file
        self.burnin = burnin
        self.data = self._parse_posterior_log()
        self.summary = self._get_summary_statistics()

        self.data['name'] = [self.log.name for _ in self.data.iterrows()]
        self.summary['name'] = [self.log.name for _ in self.summary.iterrows()]

    def _parse_posterior_log(self) -> pandas.DataFrame:
        """ Parse the posterior log avoiding using pandas.read_csv """
        with self.log.open() as posterior_data:
            header = []
            data = []
            for line in posterior_data:
                if line.startswith("#"):
                    continue
                elif line.startswith("Sample"):
                    header = line.strip().split("\t")
                else:
                    data.append(
                        [float(v) for v in line.strip().split("\t")]
                    )
        df = pandas.DataFrame(data, columns=header)
        df['Sample'] = df['Sample'].astype(int)

        total_samples = df['Sample'].values[-1]
        df = df.loc[df["Sample"] >= total_samples*self.burnin, :]

        drop_columns = [
            column for column in df.columns 
            if any(s in column for s in ('[', ']'))  # get rid of duplicate sliced columns
        ]
        df = df.drop(columns=drop_columns)

        return df
    
    def _get_summary_statistics(self, alpha: float = 0.95) -> pandas.DataFrame:
        """ 
        Get summary statistics of the posteriors

        Not computing ESS since the implementations in the available packages
        differ strongly from the estimates computed in Tracer, which is the
        standard for BEAST derived ESS computation.
        """
        
        summaries = []
        for column in self.data.columns:
            if column != 'Sample':
                posterior = self.data.loc[:, column]
                hpd_lower, hpd_upper = hdi(posterior.values, hdi_prob=alpha)
                summaries.append((
                    column, 
                    posterior.mean(), 
                    hpd_lower, 
                    hpd_upper,
                    posterior.std(), 
                    posterior.median(), 
                    posterior.min(), 
                    posterior.max(),
                ))

        return pandas.DataFrame(
            summaries, columns=[
                'Parameter',  'Mean',  'Lower HPD', 'Upper HPD', 'Standard Deviation', 'Median', 'Minimum', 'Maximum'
            ]
        )

    def _get_gridded_skyline(self, most_recent_sample_date: float):

        """ 
        Gridded skyline of the reproductive number

        Implements the `bdskytools` workflow conditioned on 
        the median tree height
        
        """

        pass