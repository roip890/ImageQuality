import pandas as pd
import random
import operator
from itertools import groupby

from utils.experiment import Experiment
from utils.experts import Experts

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

    def sample_data(self, samples, experts=Experts.All, experiment=Experiment.Random, distributions=None,
                    accuracy_function=None):

        # experiment
        if experiment == Experiment.All:
            experiment_range = range(self.num_experiments)
        elif experiment == Experiment.Random:
            experiment_range = [random.randint(0, self.num_experiments - 1)]
        else:
            experiment_range = [experiment.value]

        # experts
        if experts == Experts.All:
            experts_range = range(3)
        elif experts == Experts.Random:
            experts_range = [random.randint(0, 3)]
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

        # accuracy function
        if accuracy_function is None:
            accuracy_function = self.calculate_most_accuracy()
        # return calculations
        accuracy_function_result = accuracy_function(data)
        result = accuracy_function_result[0] if isinstance(accuracy_function_result, list) else accuracy_function_result
        payload = accuracy_function_result[1] if isinstance(accuracy_function_result, list) else {}
        # isinstance(accuracy_function_result, list)
        return result, self.group_data(data), samples, payload, data

    @staticmethod
    def calculate_rand_accuracy(data):
        return [random.randint(0, 1), {'rand': True}]

    @staticmethod
    def calculate_mean_accuracy(data):
        return sum([value[1] for value in data]) / len(data)

    @staticmethod
    def calculate_most_accuracy(next_func=None):
        def calculate_most_accuracy_helper(data):
            ones_len = len([value[1] for value in data if value[1] == 1])
            zeros_len = len([value[1] for value in data if value[1] == 0])
            if ones_len > zeros_len:
                return 1
            elif zeros_len > ones_len:
                return 0
            else:
                return next_func(data) if next_func is not None else Data.calculate_rand_accuracy(data)

        return calculate_most_accuracy_helper

    @staticmethod
    def calculate_weighted_most_accuracy(next_func=None):
        def calculate_weighted_most_accuracy_helper(data):
            # beginners
            beginners_ones_len = len(
                [value[1] for value in data if value[1] == 1 and value[0] == Experts.Beginner.value])
            beginners_zeros_len = len(
                [value[1] for value in data if value[1] == 0 and value[0] == Experts.Beginner.value])

            # mediums
            mediums_ones_len = len([value[1] for value in data if value[1] == 1 and value[0] == Experts.Medium.value])
            mediums_zeros_len = len([value[1] for value in data if value[1] == 0 and value[0] == Experts.Medium.value])

            # experts
            experts_ones_len = len([value[1] for value in data if value[1] == 1 and value[0] == Experts.Expert.value])
            experts_zeros_len = len([value[1] for value in data if value[1] == 0 and value[0] == Experts.Expert.value])

            # ones
            ones_len = (beginners_ones_len * Experts.expert_price(Experts.Beginner)) + (
                    mediums_ones_len * Experts.expert_price(Experts.Medium)) + (
                               experts_ones_len * Experts.expert_price(Experts.Expert))
            # zeros
            zeros_len = (beginners_zeros_len * Experts.expert_price(Experts.Beginner)) + (
                    mediums_zeros_len * Experts.expert_price(Experts.Medium)) + (
                                experts_zeros_len * Experts.expert_price(Experts.Expert))

            if ones_len > zeros_len:
                return 1
            elif zeros_len > ones_len:
                return 0
            else:
                return next_func(data) if next_func is not None else Data.calculate_rand_accuracy(data)

        return calculate_weighted_most_accuracy_helper

    @staticmethod
    def calculate_tie_breaker_accuracy(tie_breaker, next_func=None):
        def calculate_tie_breaker_accuracy_helper(data):
            if tie_breaker == Experts.Beginner:
                # beginners
                beginners_ones_len = len(
                    [value[1] for value in data if value[1] == 1 and value[0] == Experts.Beginner.value])
                beginners_zeros_len = len(
                    [value[1] for value in data if value[1] == 0 and value[0] == Experts.Beginner.value])
                if beginners_ones_len > beginners_zeros_len:
                    return 1
                elif beginners_zeros_len > beginners_ones_len:
                    return 0
                else:
                    return next_func(data) if next_func is not None else Data.calculate_rand_accuracy(data)
            elif tie_breaker == Experts.Medium:
                # mediums
                mediums_ones_len = len(
                    [value[1] for value in data if value[1] == 1 and value[0] == Experts.Medium.value])
                mediums_zeros_len = len(
                    [value[1] for value in data if value[1] == 0 and value[0] == Experts.Medium.value])
                if mediums_ones_len > mediums_zeros_len:
                    return 1
                elif mediums_zeros_len > mediums_ones_len:
                    return 0
                else:
                    return next_func(data) if next_func is not None else Data.calculate_rand_accuracy(data)
            elif tie_breaker == Experts.Expert:
                # experts
                experts_ones_len = len(
                    [value[1] for value in data if value[1] == 1 and value[0] == Experts.Expert.value])
                experts_zeros_len = len(
                    [value[1] for value in data if value[1] == 0 and value[0] == Experts.Expert.value])
                if experts_ones_len > experts_zeros_len:
                    return 1
                elif experts_zeros_len > experts_ones_len:
                    return 0
                else:
                    return next_func(data) if next_func is not None else Data.calculate_rand_accuracy(data)
            else:
                return next_func(data) if next_func is not None else Data.calculate_rand_accuracy(data)

        return calculate_tie_breaker_accuracy_helper

    @staticmethod
    def group_data(data):
        grouped_data = groupby(sorted(data, key=operator.itemgetter(0)), operator.itemgetter(0))
        return {Experts.expert_value_to_enum(key).name: len(list([v for k, v in group])) for key, group in grouped_data}
