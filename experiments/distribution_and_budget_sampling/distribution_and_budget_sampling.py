from pathlib import Path
import matplotlib.pyplot as plt
import time
import uuid

from utils.experiment import Experiment
from utils.experts import Experts
from utils.data import Data
from utils.terminal_colors import terminal_colors
from utils.logger import Logger


# compare sample by users number and distributions with regular budget
class DistributionAndBudgetSampling(object):
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
        self.saved_data_dir = 'experiments/distribution_and_budget_sampling/saved_data'
        Path(self.saved_data_dir).mkdir(parents=True, exist_ok=True)

    def experiment(self, show_beginners=True, show_mediums=True, show_experts=True):
        experiment_id = uuid.uuid4().hex
        experiment_dir = f'{self.saved_data_dir}/{experiment_id}'
        log_file_name = f'{experiment_dir}/log.txt'
        Path(experiment_dir).mkdir(parents=True, exist_ok=True)
        logger = Logger(log_file_name)
        logger.log(f'Experiment: DistributionAndBudgetSampling')
        logger.log(f'Num Users: {self.num_of_users}')
        logger.log(f'Num Batch: {self.num_batch}')
        logger.log(f'Budget Amount: {self.budget}')
        logger.log(f'Beginners Range: {self.beginners_range}')
        logger.log(f'Medium Range: {self.medium_range}')
        logger.log(f'Experts Range: {self.experts_range}')
        logger.log(f'Accuracy Function: {self.accuracy_function}')

        # distribution
        logger.log('Start Distribution Experiment')
        samples_averages, iterations = self.ranges_sample_data_with_budget_output(
            num_batch=self.num_batch,
            beginners_range=self.beginners_range,
            medium_range=self.medium_range,
            experts_range=self.experts_range,
            logger=logger,
        )
        logger.log('End Distribution Experiment')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # beginner
        if show_beginners:
            logger.log('Start Beginner')
            beginner_samples_averages, beginner_iterations = self.budget_sample_data(Experts.Beginner,
                                                                                     budget=self.budget,
                                                                                     num_batch=self.num_batch,
                                                                                     logger=logger)
            logger.log('End Beginner')
            logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # medium
        if show_mediums:
            logger.log('Start Medium')
            medium_samples_averages, medium_iterations = self.budget_sample_data(Experts.Medium,
                                                                                 budget=self.budget,
                                                                                 num_batch=self.num_batch,
                                                                                 logger=logger)
            logger.log('End Medium')
            logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # expert
        if show_experts:
            logger.log('Start Expert')
            expert_samples_averages, expert_iterations = self.budget_sample_data(Experts.Expert,
                                                                                 budget=self.budget,
                                                                                 num_batch=self.num_batch,
                                                                                 logger=logger)
            logger.log('End Expert')
            logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # plot
        logger.log('Start Plot And Saving Plot File')
        plt.ylabel('Sample Averages')
        plt.xlabel('Budget')
        plt.xticks(range(0, self.budget + 1, 2))
        plt.plot(iterations, samples_averages, 'o', color='red', label='Beginners: [' + ', '.join(
            [str(self.beginners_range[0]), str(self.beginners_range[-1])]) + '], Mediums: [' + ', '.join(
            [str(self.medium_range[0]), str(self.medium_range[-1])]) + '], Experts: [' + ', '.join(
            [str(self.experts_range[0]), str(self.experts_range[-1])]) + ']')
        if show_beginners:
            plt.plot(beginner_iterations, beginner_samples_averages, 'o', color='blue', label='Beginner (2 seconds)')
        if show_mediums:
            plt.plot(medium_iterations, medium_samples_averages, 'o', color='orange', label='Medium (6 seconds)')
        if show_experts:
            plt.plot(expert_iterations, expert_samples_averages, 'o', color='green', label='Expert (12 seconds)')
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
        if show_beginners:
            logger.log('Beginner Samples Averages:' + str(
                [round(value, 3) for value in beginner_samples_averages]), terminal_colors.OKGREEN)
        if show_mediums:
            logger.log('Medium Samples Averages:' + str(
                [round(value, 3) for value in medium_samples_averages]), terminal_colors.OKGREEN)
        if show_experts:
            logger.log('Expert Samples Averages:' + str(
                [round(value, 3) for value in expert_samples_averages]), terminal_colors.OKGREEN)
        logger.log('End Log Result')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

    def ranges_sample_data_with_budget_output(self, num_batch, beginners_range, medium_range, experts_range, logger):
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
                    budget = (num_beginners * Experts.expert_price(Experts.Beginner)) + (
                            num_medium * Experts.expert_price(Experts.Medium)) + (
                                     num_experts * Experts.expert_price(Experts.Expert))
                    iterations.append(budget)
        return samples_averages, iterations

    def budget_sample_data(self, experts, budget, num_batch, logger):
        samples_averages = []
        budget_iterations = []
        for i in range(1, budget + 1):
            if i % Experts.expert_price(experts) == 0:
                samples = [self.data.sample_data(samples=int(i / Experts.expert_price(experts)), experts=experts,
                                                 experiment=Experiment.Random,
                                                 accuracy_function=self.accuracy_function)[0] for j in
                           range(num_batch)]
                samples_averages.append(sum(samples) / len(samples))
                budget_iterations.append(i)
                logger.log('Iteration Num: ' + str(int(i / Experts.expert_price(experts))))
                logger.log('Budget: ' + str(i))

        return samples_averages, budget_iterations

    def test(self):
        # compare expert with combination of beginners and experts
        self.num_batch = 1000
        self.beginners_range = range(0, 1)
        self.medium_range = range(0, 1)
        self.experts_range = range(1, 30)
        # self.accuracy_function = Data.calculate_weighted_most_accuracy
        self.accuracy_function = Data.calculate_tie_breaker_accuracy(
            tie_breaker=Experts.Expert,
            next_func=Data.calculate_weighted_most_accuracy(
                next_func=Data.calculate_most_accuracy()
            ))
        # self.accuracy_function = Data.calculate_most_accuracy
        self.budget = (max(self.beginners_range) * Experts.expert_price(Experts.Beginner)) + (
                max(self.medium_range) * Experts.expert_price(Experts.Medium)) + (
                              max(self.experts_range) * Experts.expert_price(Experts.Expert))
        self.experiment(show_beginners=False, show_mediums=False, show_experts=False)
