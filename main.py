import sys
from experiments.distribution_and_budget_sampling.distribution_and_budget_sampling import DistributionAndBudgetSampling


def start(args):
    sampling_experiment = DistributionAndBudgetSampling()
    sampling_experiment.test()


start(sys.argv)
