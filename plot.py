import argparse
import functools
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


class CorePlotter(object):
    def __init__(self, data):
        self.data = data

    def __call__(self, ax, circuit):
        values = data[data['Circuit'] == circuit]
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
    ax.set_ylabel("Runtime in seconds")
    plt.savefig("weak.pdf")
