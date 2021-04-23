from pathlib import Path
import matplotlib.pyplot as plt
import time
import uuid

from utils.experiment import Experiment
from utils.experts import Experts
from utils.data import Data
from utils.terminal_colors import terminal_colors
from utils.logger import Logger


# sample by users number
class RandomSampling(object):
    def __init__(self):
        self.data = Data()
        self.start_time = time.time()
        self.num_of_users = 20
        self.budget = 100
        self.num_batch = 10000
        self.beginners_range = range(0, 20)
        self.medium_range = range(0, 1)
        self.experts_range = range(1, 2)
        self.accuracy_function = Data.calculate_most_accuracy()
        self.saved_data_dir = 'experiments/random_sampling/saved_data'
        Path(self.saved_data_dir).mkdir(parents=True, exist_ok=True)

    def experiment(self):
        experiment_id = uuid.uuid4().hex
        experiment_dir = f'{self.saved_data_dir}/{experiment_id}'
        log_file_name = f'{experiment_dir}/log.txt'
        Path(experiment_dir).mkdir(parents=True, exist_ok=True)
        logger = Logger(log_file_name)
        logger.log(f'Experiment: DistributionSampling')
        logger.log(f'Num Users: {self.num_of_users}')
        logger.log(f'Num Batch: {self.num_batch}')
        logger.log(f'Budget Amount: {self.budget}')
        logger.log(f'Beginners Range: {self.beginners_range}')
        logger.log(f'Medium Range: {self.medium_range}')
        logger.log(f'Experts Range: {self.experts_range}')
        logger.log(f'Accuracy Function: {self.accuracy_function}')

        # beginner
        logger.log('Start Beginner')
        beginner_samples_averages, beginner_iterations = self.num_of_users_sample_data(Experts.Beginner,
                                                                                       num_of_users=self.num_of_users,
                                                                                       num_batch=self.num_batch,
                                                                                       logger=logger)
        logger.log('End Beginner')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # medium
        logger.log('Start Medium')
        medium_samples_averages, medium_iterations = self.num_of_users_sample_data(Experts.Medium,
                                                                                   num_of_users=self.num_of_users,
                                                                                   num_batch=self.num_batch,
                                                                                   logger=logger)
        logger.log('End Medium')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # expert
        logger.log('Start Expert')
        expert_samples_averages, expert_iterations = self.num_of_users_sample_data(Experts.Expert,
                                                                                   num_of_users=self.num_of_users,
                                                                                   num_batch=self.num_batch,
                                                                                   logger=logger)
        logger.log('End Expert')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # plot
        logger.log('Start Plot And Saving Plot File')
        plt.ylabel('Sample Averages')
        plt.xlabel('Iterations')
        plt.plot(beginner_iterations, beginner_samples_averages, 'o', color='blue', label='Beginner (2 seconds)')
        plt.plot(medium_iterations, medium_samples_averages, 'o', color='orange', label='Medium (6 seconds)')
        plt.plot(expert_iterations, expert_samples_averages, 'o', color='green', label='Expert (12 seconds)')
        plt.legend(loc='best')
        plot_output_file_name = f'{experiment_dir}/plot.png'
        plt.savefig(plot_output_file_name)
        plt.show()
        logger.log('End Plot And Saving Plot File')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # save files
        logger.log('Start Log Result')
        logger.log('Beginner Samples Averages:' + str(
            [round(value, 3) for value in beginner_samples_averages]), terminal_colors.OKGREEN)
        logger.log('Medium Samples Averages:' + str(
            [round(value, 3) for value in medium_samples_averages]), terminal_colors.OKGREEN)
        logger.log('Expert Samples Averages:' + str(
            [round(value, 3) for value in expert_samples_averages]), terminal_colors.OKGREEN)
        logger.log('End Log Result')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

    def num_of_users_sample_data(self, experts, num_of_users, num_batch, logger):
        samples_averages = []
        iterations = range(1, num_of_users + 1)
        for i in range(1, num_of_users + 1):
            samples = [self.data.sample_data(samples=i, experts=experts, experiment=Experiment.Random,
                                             accuracy_function=self.accuracy_function)[0] for j in
                       range(num_batch)]
            samples_averages.append(sum(samples) / len(samples))
            logger.log('Iteration Num: ' + str(i))
        return samples_averages, iterations

    def test(self):
        self.num_batch = 10000
        self.num_of_users = 20
        self.experiment()
