import math
import sys
from data import Data
import matplotlib.pyplot as plt
from experts import Experts
from experiment import Experiment


class App(object):
    def __init__(self):
        self.data = Data()

    @staticmethod
    def plot(y_values, x_values, y_label, x_label):
        plt.plot(x_values, y_values)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.show()

    def sample_data(self, experts, num_iterations=50, num_batch=1000):
        samples_averages = []
        iterations = range(1, num_iterations+1)
        for i in range(1, num_iterations+1):
            samples = [self.data.sample_data(samples=i, experts=experts)[0] for j in range(num_batch)]
            samples_averages.append(sum(samples) / len(samples))
            print('Iteration Num: ' + str(i))
        return samples_averages, iterations


def start(args):

    # init app
    app = App()

    # beginner
    print('Start Beginner:')
    samples_averages, iterations = app.sample_data(Experts.Beginner, num_iterations=20, num_batch=10000)
    app.plot(samples_averages, iterations, 'Samples Averages', 'Iterations')
    print('Beginner Samples Averages:' + str([round(value, 3) for value in samples_averages]))
    print('Expert End Beginner:')

    # medium
    print('Start Medium:')
    samples_averages, iterations = app.sample_data(Experts.Medium, num_iterations=20, num_batch=10000)
    app.plot(samples_averages, iterations, 'Samples Averages', 'Iterations')
    print('Medium Samples Averages:' + str([round(value, 3) for value in samples_averages]))
    print('End Medium:')

    # expert
    print('Start Expert:')
    samples_averages, iterations = app.sample_data(Experts.Expert, num_iterations=20, num_batch=10000)
    app.plot(samples_averages, iterations, 'Samples Averages', 'Iterations')
    print('Expert Samples Averages:' + str([round(value, 3) for value in samples_averages]))
    print('End Expert:')


start(sys.argv)
