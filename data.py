import pandas as pd
from experts import Experts
from experiment import Experiment
import random
import operator
from itertools import groupby

NUM_EXPERIMENTS = 10
NUM_USERS = 50


class Data(object):
    def __init__(self):
        self.data = {
            Experts.Beginner.value: self.generate_dataframe('data/imgQuality_2.csv'),
            Experts.Medium.value: self.generate_dataframe('data/imgQuality_6.csv'),
            Experts.Expert.value: self.generate_dataframe('data/imgQuality_12.csv')
        }
        self.num_experiments = NUM_EXPERIMENTS
        self.num_users = NUM_USERS

    def generate_dataframe(self, filename):
        return pd.read_csv(filename, index_col=0).iloc[:, 2:].replace(True, 1).replace(False, 0)

    def sample_data(self, samples, experts, experiment=Experiment.All, distributions=None):

        # experiment
        if experiment == Experiment.All:
            experiment_range = range(self.num_experiments)
        else:
            experiment_range = [experiment.value]

        # experts
        if experts == Experts.All:
            experts_range = range(3)
        else:
            experts_range = [experts.value]

        # users
        users_range = range(self.num_users)

        # samples
        samples = min(samples, len(experiment_range) * len(experts_range) * len(users_range))

        # indices
        if distributions is None:
            sample_indices = random.sample(
                [(i, j, k) for i in experts_range for j in users_range for k in experiment_range], k=samples)
        else:
            sample_indices = []
            beginner_samples = min(int(samples * distributions.get(Experts.Beginner, 0)),
                                   len(experiment_range) * len(users_range))
            sample_indices.extend(random.sample(
                [(i, j, k) for i in [Experts.Beginner.value] for j in users_range for k in experiment_range],
                k=beginner_samples))
            medium_samples = min(int(samples * distributions.get(Experts.Medium, 0)),
                                 len(experiment_range) * len(users_range))
            sample_indices.extend(random.sample(
                [(i, j, k) for i in [Experts.Medium.value] for j in users_range for k in experiment_range],
                k=medium_samples))
            expert_samples = min(int(samples * distributions.get(Experts.Expert, 0)),
                                 len(experiment_range) * len(users_range))
            sample_indices.extend(random.sample(
                [(i, j, k) for i in [Experts.Expert.value] for j in users_range for k in experiment_range],
                k=expert_samples))
            samples = beginner_samples + medium_samples + expert_samples
        # sample data
        data = [(sample[0], self.data[sample[0]].iloc[sample[1]][sample[2]]) for sample in sample_indices]

        # return calculations
        return self.calculate_most_accuracy(data), self.group_data(data), samples

    @staticmethod
    def calculate_accuracy(data):
        return sum([value[1] for value in data]) / len(data)

    @staticmethod
    def calculate_most_accuracy(data):
        ones_len = len([value[1] for value in data if value[1] == 1])
        zeros_len = len([value[1] for value in data if value[1] == 0])
        if ones_len > zeros_len:
            return 1
        elif zeros_len > ones_len:
            return 0
        else:
            return random.randint(0, 1)

    @staticmethod
    def group_data(data):
        grouped_data = groupby(sorted(data, key=operator.itemgetter(0)), operator.itemgetter(0))
        return {Experts.expert_value_to_enum(key).name: len(list([v for k, v in group])) for key, group in grouped_data}
