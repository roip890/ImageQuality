import sys
from data import Data
import matplotlib.pyplot as plt
from experiment import Experiment
from experts import Experts
import time
import uuid
from terminal_colors import terminal_colors


class App(object):
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

    # sample by users number
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

    def num_of_users_sample_data(self, experts, num_of_users, num_batch):
        samples_averages = []
        iterations = range(1, num_of_users + 1)
        for i in range(1, num_of_users + 1):
            samples = [self.data.sample_data(samples=i, experts=experts, experiment=Experiment.Random, accuracy_function=self.accuracy_function)[0] for j in
                       range(num_batch)]
            samples_averages.append(sum(samples) / len(samples))
            print('Iteration Num: ' + str(i))
        return samples_averages, iterations

    # sample by budget (seconds count)
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
        plt.xlabel('Budget')
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

    def budget_sample_data(self, experts, budget, num_batch):
        samples_averages = []
        budget_iterations = []
        for i in range(1, budget + 1):
            if i % Experts.expert_price(experts) == 0:
                samples = [self.data.sample_data(samples=int(i / Experts.expert_price(experts)), experts=experts, experiment=Experiment.Random, accuracy_function=self.accuracy_function)[0] for j in
                           range(num_batch)]
                samples_averages.append(sum(samples) / len(samples))
                budget_iterations.append(i)
                print('Iteration Num: ' + str(int(i / Experts.expert_price(experts))))
                print('Budget: ' + str(i))

        return samples_averages, budget_iterations

    # sample by users number and distributions
    def third_experiment(self):
        # beginner
        print('Start Experiment')
        samples_averages, iterations = self.ranges_sample_data(
            num_batch=self.num_batch,
            beginners_range=self.beginners_range,
            medium_range=self.medium_range,
            experts_range=self.experts_range,
        )
        print('End Experiment')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # plot
        print('Start Plot And Saving Plot File')
        plt.ylabel('Sample Averages')
        plt.xlabel('Distributions')
        plt.plot(iterations, samples_averages, 'o', color='red', label='Beginners: [' + ', '.join([str(self.beginners_range[0]), str(self.beginners_range[-1])]) + '], Mediums: [' + ', '.join([str(self.medium_range[0]), str(self.medium_range[-1])]) + '], Experts: [' + ', '.join([str(self.experts_range[0]), str(self.experts_range[-1])]) + ']')
        plt.legend(loc='best')
        output_file_name = 'result_' + str(self.num_batch) + '_beginners_' + '_'.join([str(self.beginners_range[0]), str(self.beginners_range[-1])]) + '_mediums_' + '_'.join([str(self.medium_range[0]), str(self.medium_range[-1])]) + '_experts_' + '_'.join([str(self.experts_range[0]), str(self.experts_range[-1])]) + '_' + uuid.uuid4().hex
        plot_output_file_name = output_file_name + '.png'
        plt.savefig(plot_output_file_name)
        plt.show()
        print('End Plot And Saving Plot File')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # save files
        print('Start Saving Text File')
        text_output_file_name = output_file_name + '.txt'
        with open(text_output_file_name, 'w+') as output_file:
            output_file.write('Samples Averages:' + str([round(value, 3) for value in samples_averages]) + '\n')
        print('End Saving Text File')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # log
        print('Start Log Result')
        print(terminal_colors.OKGREEN + 'Samples Averages:' + str([round(value, 3) for value in samples_averages]) + terminal_colors.ENDC)
        print('End Log Result')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

    def ranges_sample_data(self, num_batch, beginners_range, medium_range, experts_range):
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
                    print('Iteration Num: ' + str(len(iterations)) + ', ' + 'Beginners: ' + str(num_beginners) + ', Medium: ' + str(num_medium) + ', Experts: ' + str(num_experts) + ', Sum: ' + str(num_samples) + ', Result: ' + str(sum(samples) / len(samples)))
                    iterations.append('\n'.join([str(num_beginners), str(num_medium), str(num_experts)]))
        return samples_averages, iterations

    # compare sample by users number and distributions with regular budget
    def fourth_experiment(self, show_beginners=True, show_mediums=True, show_experts=True):
        # distribution
        print('Start Distribution Experiment')
        samples_averages, iterations = self.ranges_sample_data_with_budget_output(
            num_batch=self.num_batch,
            beginners_range=self.beginners_range,
            medium_range=self.medium_range,
            experts_range=self.experts_range,
        )
        print('End Distribution Experiment')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # beginner
        if show_beginners:
            print('Start Beginner')
            beginner_samples_averages, beginner_iterations = self.budget_sample_data(Experts.Beginner,
                                                                              budget=self.budget,
                                                                              num_batch=self.num_batch)
            print('End Beginner')
            print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # medium
        if show_mediums:
            print('Start Medium')
            medium_samples_averages, medium_iterations = self.budget_sample_data(Experts.Medium,
                                                                                 budget=self.budget,
                                                                                 num_batch=self.num_batch)
            print('End Medium')
            print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # expert
        if show_experts:
            print('Start Expert')
            expert_samples_averages, expert_iterations = self.budget_sample_data(Experts.Expert,
                                                                                 budget=self.budget,
                                                                                 num_batch=self.num_batch)
            print('End Expert')
            print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # plot
        print('Start Plot And Saving Plot File')
        plt.ylabel('Sample Averages')
        plt.xlabel('Budget')
        plt.xticks(range(0, self.budget + 1, 2))
        plt.plot(iterations, samples_averages, 'o', color='red', label='Beginners: [' + ', '.join([str(self.beginners_range[0]), str(self.beginners_range[-1])]) + '], Mediums: [' + ', '.join([str(self.medium_range[0]), str(self.medium_range[-1])]) + '], Experts: [' + ', '.join([str(self.experts_range[0]), str(self.experts_range[-1])]) + ']')
        if show_beginners:
            plt.plot(beginner_iterations, beginner_samples_averages, 'o', color='blue', label='Beginner (2 seconds)')
        if show_mediums:
            plt.plot(medium_iterations, medium_samples_averages, 'o', color='orange', label='Medium (6 seconds)')
        if show_experts:
            plt.plot(expert_iterations, expert_samples_averages, 'o', color='green', label='Expert (12 seconds)')
        plt.legend(loc='best')
        output_file_name = 'result_' + str(self.num_batch) + '_beginners_' + '_'.join([str(self.beginners_range[0]), str(self.beginners_range[-1])]) + '_mediums_' + '_'.join([str(self.medium_range[0]), str(self.medium_range[-1])]) + '_experts_' + '_'.join([str(self.experts_range[0]), str(self.experts_range[-1])]) + '_' + uuid.uuid4().hex
        plot_output_file_name = output_file_name + '.png'
        plt.savefig(plot_output_file_name)
        plt.show()
        print('End Plot And Saving Plot File')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # save files
        print('Start Saving Text File')
        text_output_file_name = output_file_name + '.txt'
        with open(text_output_file_name, 'w+') as output_file:
            output_file.write('Samples Averages:' + str([round(value, 3) for value in samples_averages]) + '\n')
            if show_beginners:
                output_file.write('Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]) + '\n')
            if show_mediums:
                output_file.write('Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]) + '\n')
            if show_experts:
                output_file.write('Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]) + '\n')
        print('End Saving Text File')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

        # log
        print('Start Log Result')
        print(terminal_colors.OKGREEN + 'Samples Averages:' + str([round(value, 3) for value in samples_averages]) + terminal_colors.ENDC)
        if show_beginners:
            print(terminal_colors.OKGREEN + 'Beginner Samples Averages:' + str([round(value, 3) for value in beginner_samples_averages]) + terminal_colors.ENDC)
        if show_mediums:
            print(terminal_colors.OKGREEN + 'Medium Samples Averages:' + str([round(value, 3) for value in medium_samples_averages]) + terminal_colors.ENDC)
        if show_experts:
            print(terminal_colors.OKGREEN + 'Expert Samples Averages:' + str([round(value, 3) for value in expert_samples_averages]) + terminal_colors.ENDC)
        print('End Log Result')
        print('Time elapsed: ' + str(time.time() - self.start_time) + ' seconds.')

    def ranges_sample_data_with_budget_output(self, num_batch, beginners_range, medium_range, experts_range):
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
                    print('Iteration Num: ' + str(len(iterations)) + ', ' + 'Beginners: ' + str(num_beginners) + ', Medium: ' + str(num_medium) + ', Experts: ' + str(num_experts) + ', Sum: ' + str(num_samples) + ', Result: ' + str(sum(samples) / len(samples)))
                    budget = (num_beginners * Experts.expert_price(Experts.Beginner)) + (num_medium * Experts.expert_price(Experts.Medium)) + (num_experts * Experts.expert_price(Experts.Expert))
                    iterations.append(budget)
        return samples_averages, iterations


def start(args):
    # init app
    app = App()

    # first experiment
    # app.num_batch = 10000
    # app.num_of_users = 20
    # app.first_experiment()

    # second experiment
    # app.num_batch = 10000
    # app.budget = 100
    # app.second_experiment()

    # third experiment
    # app.num_batch = 1000
    # app.beginners_range = range(0, 10)
    # app.medium_range = range(0, 1)
    # app.experts_range = range(1, 2)
    # app.accuracy_function = Data.calculate_weighted_most_accuracy
    # app.third_experiment()

    # compare expert with combination of beginners and experts
    app.num_batch = 10000
    app.beginners_range = range(1, 2)
    app.medium_range = range(0, 1)
    app.experts_range = range(2, 3)
    # app.accuracy_function = Data.calculate_weighted_most_accuracy
    app.accuracy_function = Data.calculate_most_accuracy_with_tie_breaker(tie_breaker=Experts.Expert)
    # app.accuracy_function = Data.calculate_most_accuracy
    app.budget = (max(app.beginners_range) * Experts.expert_price(Experts.Beginner)) + (max(app.medium_range) * Experts.expert_price(Experts.Medium)) + (max(app.experts_range) * Experts.expert_price(Experts.Expert))
    print(app.budget)
    app.fourth_experiment(show_beginners=False, show_mediums=False)

    # compare expert with combination of mediums and experts
    # app.num_batch = 1000
    # app.beginners_range = range(0, 1)
    # app.medium_range = range(0, 13)
    # app.experts_range = range(1, 2)
    # app.accuracy_function = Data.calculate_weighted_most_accuracy
    # app.accuracy_function = Data.calculate_most_accuracy_with_tie_breaker(tie_breaker=Experts.Expert)
    # # app.accuracy_function = Data.calculate_most_accuracy
    # app.budget = (max(app.beginners_range) * Experts.expert_price(Experts.Beginner)) + (max(app.medium_range) * Experts.expert_price(Experts.Medium)) + (max(app.experts_range) * Experts.expert_price(Experts.Expert))
    # app.fourth_experiment(show_beginners=False, show_mediums=False)
    #
    # # compare mediums with combination of beginners and mediums
    # app.num_batch = 10000
    # app.beginners_range = range(0, 4)
    # app.medium_range = range(1, 2)
    # app.experts_range = range(0, 1)
    # app.accuracy_function = Data.calculate_weighted_most_accuracy
    # # app.accuracy_function = Data.calculate_most_accuracy_with_tie_breaker(tie_breaker=Experts.Medium)
    # # app.accuracy_function = Data.calculate_most_accuracy
    # app.budget = (max(app.beginners_range) * Experts.expert_price(Experts.Beginner)) + (max(app.medium_range) * Experts.expert_price(Experts.Medium)) + (max(app.experts_range) * Experts.expert_price(Experts.Expert))
    # app.fourth_experiment(show_beginners=False, show_experts=False)


start(sys.argv)
