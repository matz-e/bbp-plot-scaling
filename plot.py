import argparse
import functools
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import pandas as pd


def to_sec(s):
    """Convert a string to seconds

    >>> to_sec("1:00:00")
    3600
    >>> to_sec("5:01")
    301
    """
    def _conv(a, b):
        return a * 60 + b
    return functools.reduce(_conv, (int(n) for n in s.split(":")))


def load_data(fn):
    data = pd.read_csv(fn)
    data['time total'] = [to_sec(s) for s in data['time total']]
    return data


def to_time(x, pos=None):
    """Convert seconds to time string

    >>> to_time(3600)
    '1:00:00'
    >>> to_time(301)
    '5:01'
    >>> to_time(301.0)
    '5:01'
    """
    res = []
    while x > 0:
        res.append(x % 60)
        x //= 60
    return ":".join("{:02}".format(int(i)) for i in reversed(res)).lstrip("0")


class CorePlotter(object):
    def __init__(self, data):
        self.data = data

    def __call__(self, ax, circuit):
        values = self.data[self.data['Circuit'] == circuit]
        ax = values.plot(x='total # of cores',
                         y='time total',
                         kind='scatter',
                         label=circuit,
                         ax=ax)
        return ax


if __name__ == '__main__':
    parser = argparse.ArgumentParser("produce scaling plots")
    parser.add_argument("filename", help="file containing data in CSV format")
    args = parser.parse_args()

    data = load_data(args.filename)
    circuits = data['Circuit'].unique()
    ax = functools.reduce(CorePlotter(data), circuits, None)
    ax.set_title("Weak Scaling")
    ax.set_xlabel("Number of cores")
    ax.set_xscale('log', basex=2)
    ax.set_ylabel("Runtime")
    ax.yaxis.set_major_formatter(FuncFormatter(to_time))
    plt.savefig("weak.pdf", bbox_inches='tight')
