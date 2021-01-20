import matplotlib.pyplot as plt

beginner = [0.649, 0.658, 0.724, 0.728, 0.766, 0.768, 0.811, 0.806, 0.841, 0.844, 0.862, 0.865, 0.878, 0.882, 0.899, 0.898, 0.913, 0.913, 0.925, 0.927]
medium = [0.776, 0.777, 0.876, 0.873, 0.92, 0.928, 0.955, 0.956, 0.972, 0.974, 0.98, 0.981, 0.989, 0.987, 0.993, 0.993, 0.993, 0.995, 0.998, 0.998]
expert = [0.863, 0.866, 0.947, 0.951, 0.982, 0.983, 0.993, 0.991, 0.997, 0.996, 0.999, 0.999, 0.999, 0.999, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def plot(y_values, x_values, y_label, x_label):
    plt.plot(x_values, y_values)


def show_plot():
    plt.show()


plt.ylabel('Sample Averages')
plt.xlabel('Iterations')
plt.plot(range(1, 21), beginner, color='orange', label='Beginner (2 seconds)')
plt.plot(range(1, 21), medium, color='green', label='Medium (6 seconds)')
plt.plot(range(1, 21), expert, color='blue', label='Expert (12 seconds)')
plt.legend(loc='best')
plt.show()
