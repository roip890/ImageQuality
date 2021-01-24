import sys
from data import Data
import matplotlib.pyplot as plt
from experiment import Experiment
from experts import Experts
import time
import uuid


class App(object):
    def __init__(self):
        self.data = Data()
        self.start_time = time.time()
        self.num_of_users = 20
        self.budget = 100
        self.num_batch = 10000

    def num_of_users_sample_data(self, experts, num_of_users, num_batch):
        samples_averages = []
        iterations = range(1, num_of_users + 1)
        for i in range(1, num_of_users + 1):
            samples = [self.data.sample_data(samples=i, experts=experts, experiment=Experiment.Random)[0] for j in
                       range(num_batch)]
            samples_averages.append(sum(samples) / len(samples))
            print('Iteration Num: ' + str(i))
        return samples_averages, iterations

    def budget_sample_data(self, experts, budget, num_batch):
        samples_averages = []
        budget_iterations = []
        for i in range(1, budget + 1):
            if i % Experts.expert_price(experts) == 0:
                samples = [self.data.sample_data(samples=int(i / Experts.expert_price(experts)), experts=experts, experiment=Experiment.Random)[0] for j in
                           range(num_batch)]
                samples_averages.append(sum(samples) / len(samples))
                budget_iterations.append(i)
                print('Iteration Num: ' + str(int(i / Experts.expert_price(experts))))
                print('Budget: ' + str(i))

        return samples_averages, budget_iterations

    def first_experiment(self):
        # beginner
        print('Start Beginner')
        beginner_samples_averages, beginner_iterations = self.num_of_users_sample_data(Experts.Beginner,
                                                                                       num_of_users=self.num_of_users,
                                                                                       num_batch=self.num_batch)
        print('End Beginner')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # medium
        print('Start Medium')
        medium_samples_averages, medium_iterations = self.num_of_users_sample_data(Experts.Medium,
                                                                                   num_of_users=self.num_of_users,
                                                                                   num_batch=self.num_batch)
        print('End Medium')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # expert
        print('Start Expert')
        expert_samples_averages, expert_iterations = self.num_of_users_sample_data(Experts.Expert,
                                                                                   num_of_users=self.num_of_users,
                                                                                   num_batch=self.num_batch)
        print('End Expert')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # plot
        print('Start Plot And Saving Plot File')
        plt.ylabel('Sample Averages')
        plt.xlabel('Iterations')
        plt.plot(beginner_iterations, beginner_samples_averages, 'o', color='blue', label='Beginner (2 seconds)')
        plt.plot(medium_iterations, medium_samples_averages, 'o', color='orange', label='Medium (6 seconds)')
        plt.plot(expert_iterations, expert_samples_averages, 'o', color='green', label='Expert (12 seconds)')
        plt.legend(loc='best')
        output_file_name = 'result_' + str(self.num_batch) + '_count_' + str(self.num_of_users) + '_users_' + uuid.uuid4().hex
        plot_output_file_name = output_file_name + '.png'
        plt.savefig(plot_output_file_name)
        plt.show()
        print('End Plot And Saving Plot File')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # save files
        print('Start Saving Text File')
        text_output_file_name = output_file_name + '.txt'
        with open(text_output_file_name, 'w+') as output_file:
            output_file.write(
                'Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]) + '\n')
            output_file.write(
                'Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]) + '\n')
            output_file.write(
                'Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]) + '\n')
        print('End Saving Text File')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # log
        print('Start Log Result')
        print('Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]))
        print('Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]))
        print('Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]))
        print('End Log Result')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

    def second_experiment(self):
        # beginner
        print('Start Beginner')
        beginner_samples_averages, beginner_iterations = self.budget_sample_data(Experts.Beginner,
                                                                          budget=self.budget,
                                                                          num_batch=self.num_batch)
        print('End Beginner')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # medium
        print('Start Medium')
        medium_samples_averages, medium_iterations = self.budget_sample_data(Experts.Medium,
                                                                             budget=self.budget,
                                                                             num_batch=self.num_batch)
        print('End Medium')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # expert
        print('Start Expert')
        expert_samples_averages, expert_iterations = self.budget_sample_data(Experts.Expert,
                                                                             budget=self.budget,
                                                                             num_batch=self.num_batch)
        print('End Expert')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # plot
        print('Start Plot And Saving Plot File')
        plt.ylabel('Sample Averages')
        plt.xlabel('Iterations')
        plt.plot(beginner_iterations, beginner_samples_averages, 'o', color='blue', label='Beginner (2 seconds)')
        plt.plot(medium_iterations, medium_samples_averages, 'o', color='orange', label='Medium (6 seconds)')
        plt.plot(expert_iterations, expert_samples_averages, 'o', color='green', label='Expert (12 seconds)')
        plt.legend(loc='best')
        output_file_name = 'result_' + str(self.num_batch) + '_count_' + str(self.budget) + '_budget_' + uuid.uuid4().hex
        plot_output_file_name = output_file_name + '.png'
        plt.savefig(plot_output_file_name)
        plt.show()
        print('End Plot And Saving Plot File')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # save files
        print('Start Saving Text File')
        text_output_file_name = output_file_name + '.txt'
        with open(text_output_file_name, 'w+') as output_file:
            output_file.write(
                'Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]) + '\n')
            output_file.write(
                'Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]) + '\n')
            output_file.write(
                'Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]) + '\n')
        print('End Saving Text File')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # log
        print('Start Log Result')
        print('Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]))
        print('Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]))
        print('Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]))
        print('End Log Result')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')


def start(args):
    # init app
    app = App()

    # first experiment
    app.num_batch = 10000
    app.num_of_users = 20
    # app.first_experiment()

    # second experiment
    app.num_batch = 10000
    app.budget = 100
    app.second_experiment()


start(sys.argv)
