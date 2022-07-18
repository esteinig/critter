import re
import pandas
import seaborn as sns
from typing import List, Optional
from pathlib import Path
from matplotlib import pyplot as plt
from critter.diagnostic import PosteriorDiagnostic
from critter.utils import get_float_dates, read_dates

BDSKY_KEEP = ("becomeUninfectiousRate", "samplingProportion", "reproductiveNumber", "clockRate")


def plot_bdsky_posterior_summary(
        posterior: PosteriorDiagnostic,
        posterior_prior: Optional[PosteriorDiagnostic],
        output: Path
):

    keep = [column for column in posterior.data.columns if column.startswith(BDSKY_KEEP)]

    fig, axes = plt.subplots(
        nrows=len(keep), ncols=1, figsize=(14, 10)
    )
    styles = {'color': 'black'}
    for i, column in enumerate(keep):

        data = posterior.data[column]
        sns.kdeplot(data, ax=axes[i], fill=True, **styles)
        if posterior_prior is not None:
            data2 = posterior_prior.data[column]
            sns.kdeplot(data2, ax=axes[i], **styles)
        plt.xlabel(f"\n{column}")
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

    plt.tight_layout()
    fig.savefig(output)


def plot_equal_re_intervals(posterior_diagnostic: PosteriorDiagnostic, output: Path, last_sample: float = None):

    """ Dispaly mean reproductive number + 95% HPD across time slices of equal size """

    data_frame = []
    for _, row in posterior_diagnostic.summary.iterrows():
        if 'reproductiveNumber' in row['Parameter']:
            
            try:
                interval = re.findall(r'[0-9]+', row['Parameter'])[0]
            except IndexError:
                raise IndexError('Could not find the interval number in reproductiveNumber')

            data_frame.append([interval, row['Mean'], row['Lower HPD'], row['Upper HPD']])

    df = pandas.DataFrame(data_frame, columns=['Interval', 'Mean', 'Lower', 'Upper'])

    if last_sample:
        # Scale intervals based on mean tree height
        # should be used only for equally sized intervals
        tree_height = posterior_diagnostic.summary.loc[
            posterior_diagnostic.summary['Parameter'] == 'TreeHeight', 'Mean'
        ].values[0]
        tree_start = last_sample - tree_height
        interval_size = tree_height / len(df)
        
        interval_labels = []
        interval_start = tree_start
        for _, row in df.iterrows():
            interval_stop = interval_start+interval_size
            label = f"\n{round(interval_start, 2)} - {round(interval_stop, 2)}"
            interval_start = interval_stop
            interval_labels.append(label)
    else:
        interval_labels = df['Interval'].tolist()

    fig, axes = plt.subplots(
        nrows=1, ncols=1, figsize=(14, 10)
    )

    ax = sns.pointplot(x='Interval', y='Mean', data=df, ci=None, ax=axes, join=False, color="black")

    # Find the x,y coordinates for each point
    x_coords = []
    y_coords = []
    for point_pair in ax.collections:
        for x, y in point_pair.get_offsets():
            x_coords.append(x)
            y_coords.append(y)

    # Calculate the lenght of the error bars around the mean
    lower = []
    upper = []
    for _, row in df.iterrows():
        lower.append(row['Mean'] - row['Lower'])
        upper.append(row['Upper'] - row['Mean'])

    ax.errorbar(x_coords, y_coords, yerr=[lower, upper], fmt=' ', zorder=-1, ecolor="black")
    plt.axhline(y=1.0, color='black', linestyle='--')

    ax.set_ylim(ymin=0)
    ax.set_xticklabels(interval_labels)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel("Mean reproductive number\n")
    plt.xlabel("")
    plt.tight_layout()
    fig.savefig(output)


def plot_sample_date_distribution(date_files: List[Path], datefmt: bool = False, equal_slices: int = 0, output: Path = "date_density.png"):

    nrows = len(date_files)
    fig, axes = plt.subplots(
        nrows=nrows, ncols=1, figsize=(14, 10*(0.5*nrows)), sharex=True
    )

    for i, date_file in enumerate(date_files):

        dates = read_dates(date_file=date_file)
        if datefmt:
            dates = get_float_dates(dates=dates)
        
        data = pandas.DataFrame.from_records(list(dates.items()), columns=['name', 'date'])
        data = data.astype({'name': str, 'date': float})

        interval_change_points = []
        if equal_slices > 0:
            min_date, max_date = data.date.min(), data.date.max()
            interval_size = (max_date-min_date) / equal_slices
            current_date = min_date
            interval_change_points.append(min_date)
            for _ in range(equal_slices):
                current_date += interval_size
                interval_change_points.append(current_date)
  
        sns.kdeplot(data=data, x="date", ax=axes[i])
        a2 = sns.rugplot(data=data, x="date", ax=axes[i])
        a2.set_ylabel("")
        a2.set_title(date_file.name)
        axes[i].xaxis.set_tick_params(labelbottom=True)
        for cp in interval_change_points:
            axes[i].axvline(cp, color='black')

    plt.xlabel("")
    plt.tight_layout()
    fig.savefig(output)


class TreeView:

    def __init__(self, tree_file: Path, data_file: Path = None):
        
        self.tree_file = tree_file
        self.data_file = data_file

        self.newick: str = None

    def _read_newick(self):

        with self.file.open() as tree_file:
            self.newick = tree_file.readline().strip()

    def _read_data(self):

        self.data = pandas.read_csv(self.data_file, sep='\t', header=0)

    def draw(self, clusters: str = None, output: Path = 'tree.png', **kwargs):

        pass