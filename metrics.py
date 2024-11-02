import matplotlib.pyplot as plt

# Example CPU utilization data for plotting
cpu_data = [50, 55, 60, 80, 90]  # Simulated data points

plt.plot(cpu_data, label="CPU Utilization")
plt.xlabel("Time")
plt.ylabel("CPU (%)")
plt.legend()
plt.show()
