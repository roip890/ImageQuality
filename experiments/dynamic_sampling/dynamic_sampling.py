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
class DynamicSampling(object):
    def __init__(self):
        self.data = Data()
        self.start_time = time.time()
        self.num_of_users = 20
        self.budget = 100
        self.num_batch = 10000
        self.num_epochs = 10
        self.num_beginners = 0
        self.num_medium = 0
        self.num_experts = 1
        self.accuracy_function = Data.calculate_most_accuracy()
        self.saved_data_dir = 'experiments/dynamic_sampling/saved_data'
        self.tie_breaker = Experts.Beginner
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
        logger.log(f'Num Epochs: {self.num_epochs}')
        logger.log(f'Budget Amount: {self.budget}')
        logger.log(f'Num Beginners: {self.num_beginners}')
        logger.log(f'Num Medium: {self.num_medium}')
        logger.log(f'Num Experts: {self.num_experts}')
        logger.log(f'Accuracy Function: {self.accuracy_function}')

        # experiment
        logger.log('Start Experiment with Tie Breaker')
        samples_averages_with_tie_breaker = self.ranges_sample_data(
            num_beginners=self.num_beginners,
            num_medium=self.num_medium,
            num_experts=self.num_experts,
            tie_breaker=self.tie_breaker,
            logger=logger
        )
        logger.log('End Experiment with Tie Breaker')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # experiment
        logger.log('Start Experiment without Tie Breaker')
        samples_averages_without_tie_breaker = self.ranges_sample_data(
            num_beginners=self.num_beginners,
            num_medium=self.num_medium,
            num_experts=self.num_experts,
            tie_breaker=None,
            logger=logger
        )
        logger.log('End Experiment without Tie Breaker')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # plot
        logger.log('Start Plot And Saving Plot File')
        plt.ylabel('Sample Averages')
        plt.xlabel('Distributions')
        plt.title('Beginners: [' + ', '.join(
            [str(self.num_beginners)]) + '], Mediums: [' + ', '.join(
            [str(self.num_medium)]) + '], Experts: [' + ', '.join(
            [str(self.num_experts)]) + ']')
        plt.plot(range(self.num_epochs), samples_averages_with_tie_breaker, 'o', color='red',
                 label='with Tie Breaker of ' + str(self.tie_breaker))
        plt.plot(range(self.num_epochs), samples_averages_without_tie_breaker, 'o', color='blue',
                 label='without Tie Breaker')
        plt.legend(loc='best')
        plot_output_file_name = f'{experiment_dir}/plot.png'
        plt.savefig(plot_output_file_name)
        plt.show()
        logger.log('End Plot And Saving Plot File')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # save files
        logger.log('Start Log Result')
        logger.log('Samples Averages with Tie breaker:' + str(
            [round(value, 3) for value in samples_averages_with_tie_breaker]), terminal_colors.OKGREEN)
        logger.log('Samples Averages without Tie breaker:' + str(
            [round(value, 3) for value in samples_averages_without_tie_breaker]), terminal_colors.OKGREEN)
        logger.log('End Log Result')
        logger.log('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

    def ranges_sample_data(self, num_beginners, num_medium, num_experts, tie_breaker, logger):
        samples_averages = []
        samples = []
        tie_breaker_counts = []
        for i in range(self.num_epochs):
            for j in range(self.num_batch):
                num_samples = num_beginners + num_medium + num_experts
                result = self.data.sample_data(samples=num_samples, experiment=Experiment.Random, distributions={
                    Experts.Beginner: num_beginners / num_samples,
                    Experts.Medium: num_medium / num_samples,
                    Experts.Expert: num_experts / num_samples
                }, accuracy_function=self.accuracy_function)
                if tie_breaker is None or 'rand' not in result[3] or not result[3]['rand']:
                    samples.append(result[0])
                    tie_breaker_counts.append(0)
                else:
                    tie_breaker_count = 1
                    while True:
                        tb_num_samples = num_samples + tie_breaker_count
                        tb_result = self.data.sample_data(samples=tb_num_samples, experiment=Experiment.Random,
                                                          distributions={
                                                              Experts.Beginner: ((
                                                                  tie_breaker_count if tie_breaker == Experts.Beginner else 0)) / tb_num_samples,
                                                              Experts.Medium: ((
                                                                  tie_breaker_count if tie_breaker == Experts.Medium else 0)) / tb_num_samples,
                                                              Experts.Expert: ((
                                                                  tie_breaker_count if tie_breaker == Experts.Expert else 0)) / tb_num_samples
                                                          }, accuracy_function=self.accuracy_function)
                        tb_data = [*result[4], *tb_result[4]]
                        tb_acc_result = self.accuracy_function(tb_data)
                        tb_acc_result_result = tb_acc_result[0] if isinstance(tb_acc_result, list) else tb_acc_result
                        tb_acc_result_payload = tb_acc_result[1] if isinstance(tb_acc_result, list) else {}
                        if 'rand' not in tb_acc_result_payload or not tb_acc_result_payload['rand']:
                            samples.append(tb_acc_result_result)
                            tie_breaker_counts.append(tie_breaker_count)
                            break
                        tie_breaker_count += 1
            samples_averages.append(sum(samples) / len(samples))
            logger.log(', '.join([
                'Epoch Num: ' + str(i),
                'Beginners: ' + str(num_beginners),
                'Medium: ' + str(num_medium),
                'Experts: ' + str(num_experts),
                'Tie Breakers: ' + str(sum(tie_breaker_counts) / len(tie_breaker_counts)) if tie_breaker else '',
                'Max Tie Breakers: ' + str(max(tie_breaker_counts)) if tie_breaker is not None else '',
                'Result: ' + str(sum(samples) / len(samples))
            ]), terminal_colors.OKBLUE)
        return samples_averages

    def test(self):
        self.num_batch = 10000
        self.num_epochs = 100
        self.num_beginners = 0
        self.num_medium = 0
        self.num_experts = 2
        self.accuracy_function = Data.calculate_weighted_most_accuracy()
        self.tie_breaker = Experts.Beginner
        self.experiment()
