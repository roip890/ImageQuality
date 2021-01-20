import sys
from data import Data
import matplotlib.pyplot as plt
from experts import Experts
import time


class App(object):
    def __init__(self):
        self.data = Data()

    @staticmethod
    def plot(y_values, x_values, y_label, x_label):
        plt.plot(x_values, y_values)
        plt.ylabel(y_label)
        plt.xlabel(x_label)

    @staticmethod
    def show_plot():
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

    # start time
    start_time = time.time()
    num_iterations = 50
    num_batch = 10000
    output_file_name = 'mean_10000.txt'

    # init app
    app = App()

    # beginner
    print('Start Beginner')
    beginner_samples_averages, beginner_iterations = app.sample_data(Experts.Beginner, num_iterations=num_iterations, num_batch=num_batch)
    # app.plot(beginner_samples_averages, beginner_iterations, 'Samples Averages', 'Iterations')
    # print('Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]))
    print('Expert End Beginner')
    print('Time elapsed: ' + str(time.time() - start_time) + ' seconds.')

    # medium
    print('Start Medium')
    medium_samples_averages, medium_iterations = app.sample_data(Experts.Medium, num_iterations=num_iterations, num_batch=num_batch)
    # app.plot(medium_samples_averages, medium_iterations, 'Samples Averages', 'Iterations')
    # print('Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]))
    print('End Medium')
    print('Time elapsed: ' + str(time.time() - start_time) + ' seconds.')

    # expert
    print('Start Expert')
    expert_samples_averages, expert_iterations = app.sample_data(Experts.Expert, num_iterations=num_iterations, num_batch=num_batch)
    # app.plot(expert_samples_averages, expert_iterations, 'Samples Averages', 'Iterations')
    # print('Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]))
    print('End Expert')
    print('Time elapsed: ' + str(time.time() - start_time) + ' seconds.')

    # plot
    print('Start Plot')
    app.plot(beginner_samples_averages, beginner_iterations, 'Samples Averages', 'Iterations')
    app.plot(medium_samples_averages, medium_iterations, 'Samples Averages', 'Iterations')
    app.plot(expert_samples_averages, expert_iterations, 'Samples Averages', 'Iterations')
    print('Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]))
    print('Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]))
    print('Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]))
    app.show_plot()
    print('End Plot')
    print('Time elapsed: ' + str(time.time() - start_time) + ' seconds.')
    with open(output_file_name, 'w+') as output_file:
        output_file.write('Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]) + '\n')
        output_file.write('Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]) + '\n')
        output_file.write('Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]) + '\n')


start(sys.argv)
