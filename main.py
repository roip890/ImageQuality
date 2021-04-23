import sys
from experiments.distribution_and_budget_sampling.distribution_and_budget_sampling import DistributionAndBudgetSampling
from experiments.dynamic_sampling.dynamic_sampling import DynamicSampling


def start(args):
    sampling_experiment = DynamicSampling()
    sampling_experiment.test()


start(sys.argv)
