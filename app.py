import sys
from data import Data
import matplotlib.pyplot as plt
from experts import Experts
from experiment import Experiment


class App(object):
    def __init__(self):
        self.data = Data()


def start(args):

    # init app
    app = App()

    # run first experiment
    accuracy, distribution, samples = app.data.sample_data(
        samples=500,
        experiment=Experiment.All,
        experts=Experts.All,
        distributions={
           Experts.Beginner: 0.2,
           Experts.Medium: 0.3,
           Experts.Expert: 0.5
        })

    print('Accuracy: ' + str(accuracy))
    print('Distribution: ' + str(distribution))
    print('Samples: ' + str(samples))


start(sys.argv)
