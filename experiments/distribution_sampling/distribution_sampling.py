from pathlib import Path
import matplotlib.pyplot as plt
import time
import uuid

from utils.experiment import Experiment
from utils.experts import Experts
from utils.data import Data
from utils.terminal_colors import terminal_colors
from utils.logger import Logger


# sample by users number and distributions
class DistributionSampling(object):
    def __init__(self):
        self.data = Data()
        self.start_time = time.time()
        self.num_of_users = 20
        self.budget = 100
        self.num_batch = 10000
        self.beginners_range = range(0, 20)
        self.medium_range = range(0, 1)
        self.experts_range = range(1, 2)
        self.accuracy_function = Data.calculate_most_accuracy
        self.saved_data_dir = 'experiments/distribution_sampling/saved_data'
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
        logger.log(f'Num Budget: {self.beginners_range}')
        logger.log(f'Num Budget: {self.medium_range}')
        logger.log(f'Num Budget: {self.experts_range}')
        logger.log(f'Num Budget: {self.accuracy_function}')

        # beginner
        logger.log('Start Experiment')
        samples_averages, iterations = self.ranges_sample_data(
            num_batch=self.num_batch,
            beginners_range=self.beginners_range,
            medium_range=self.medium_range,
            experts_range=self.experts_range,
            logger=logger
        )
        logger.log('End Experiment')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # plot
        logger.log('Start Plot And Saving Plot File')
        plt.ylabel('Sample Averages')
        plt.xlabel('Distributions')
        plt.plot(iterations, samples_averages, 'o', color='red', label='Beginners: [' + ', '.join(
            [str(self.beginners_range[0]), str(self.beginners_range[-1])]) + '], Mediums: [' + ', '.join(
            [str(self.medium_range[0]), str(self.medium_range[-1])]) + '], Experts: [' + ', '.join(
            [str(self.experts_range[0]), str(self.experts_range[-1])]) + ']')
        plt.legend(loc='best')
        plot_output_file_name = f'{experiment_dir}/plot.png'
        plt.savefig(plot_output_file_name)
        plt.show()
        logger.log('End Plot And Saving Plot File')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # save files
        logger.log('Start Log Result')
        logger.log('Samples Averages:' + str(
            [round(value, 3) for value in samples_averages]), terminal_colors.OKGREEN)
        logger.log('End Log Result')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

    def ranges_sample_data(self, num_batch, beginners_range, medium_range, experts_range, logger):
        samples_averages = []
        iterations = []
        for num_beginners in beginners_range:
            for num_medium in medium_range:
                for num_experts in experts_range:
                    num_samples = num_beginners + num_medium + num_experts
                    samples = [self.data.sample_data(samples=num_samples, experiment=Experiment.Random, distributions={
                        Experts.Beginner: num_beginners / num_samples,
                        Experts.Medium: num_medium / num_samples,
                        Experts.Expert: num_experts / num_samples
                    }, accuracy_function=self.accuracy_function)[0] for i in range(num_batch)]
                    samples_averages.append(sum(samples) / len(samples))
                    logger.log('Iteration Num: ' + str(len(iterations)) + ', ' + 'Beginners: ' + str(
                        num_beginners) + ', Medium: ' + str(num_medium) + ', Experts: ' + str(
                        num_experts) + ', Sum: ' + str(num_samples) + ', Result: ' + str(sum(samples) / len(samples)))
                    iterations.append('\n'.join([str(num_beginners), str(num_medium), str(num_experts)]))
        return samples_averages, iterations

    def test(self):
        self.num_batch = 1000
        self.beginners_range = range(0, 10)
        self.medium_range = range(0, 1)
        self.experts_range = range(1, 2)
        self.accuracy_function = Data.calculate_weighted_most_accuracy
        self.experiment()
