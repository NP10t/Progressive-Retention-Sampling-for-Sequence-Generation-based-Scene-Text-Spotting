import matplotlib.pyplot as plt
import numpy as np

# Data extraction
data = [
    [4, 3, 73.3],
    [4, 5, 73.8],
    [2, 4, 73.9],
    [3, 4, 73.3],
    [4, 4, 74.2],
    [5, 4, 74.5],
    [6, 4, 74.2]
]

# Separate data for k (when n=4) and n (when k=4)
k_data = [(row[0], row[2]) for row in data if row[1] == 4]
n_data = [(row[1], row[2]) for row in data if row[0] == 4]

# Sort data
k_data.sort(key=lambda x: x[0])
n_data.sort(key=lambda x: x[0])

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot H-mean vs k (n=4)
k_values, h_mean_k = zip(*k_data)
ax1.plot(k_values, h_mean_k, marker='o')
ax1.set_xlabel('k')
ax1.set_ylabel('H-mean')
ax1.set_title('H-mean vs k (n=4)')
ax1.grid(True)
ax1.set_xticks(k_values)  # Set x-ticks to only use values from the data

# Plot H-mean vs n (k=4)
n_values, h_mean_n = zip(*n_data)
ax2.plot(n_values, h_mean_n, marker='o')
ax2.set_xlabel('n')
ax2.set_ylabel('H-mean')
ax2.set_title('H-mean vs n (k=4)')
ax2.grid(True)
ax2.set_xticks(n_values)  # Set x-ticks to only use values from the data

# Adjust layout
plt.tight_layout()

# Save as PDF
plt.savefig('gss_hyperparameter_plots.pdf')
print("Plot saved as 'gss_hyperparameter_plots.pdf'")

# If you still want to display the plot, uncomment the next line
# plt.show()


# import matplotlib.pyplot as plt
# import numpy as np

# # Data extraction
# data = [
#     [4, 3, 78.9, 68.5, 73.3],
#     [4, 5, 78.6, 69.4, 73.8],
#     [2, 4, 80.0, 68.8, 73.9],
#     [3, 4, 79.2, 68.2, 73.3],
#     [4, 4, 80.1, 69.0, 74.2],
#     [5, 4, 80.5, 69.3, 74.5],
#     [6, 4, 79.1, 69.8, 74.2]
# ]

# # Separate data for k (when n=4) and n (when k=4)
# k_data = [(row[0], row[2], row[3], row[4]) for row in data if row[1] == 4]
# n_data = [(row[1], row[2], row[3], row[4]) for row in data if row[0] == 4]

# # Sort data
# k_data.sort(key=lambda x: x[0])
# n_data.sort(key=lambda x: x[0])

# # Plotting
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# # Plot metrics vs k (n=4)
# k_values, precision_k, recall_k, hmean_k = zip(*k_data)
# ax1.plot(k_values, precision_k, marker='o', label='Precision')
# ax1.plot(k_values, recall_k, marker='s', label='Recall')
# ax1.plot(k_values, hmean_k, marker='^', label='H-mean')
# ax1.set_xlabel('k')
# ax1.set_ylabel('Score')
# ax1.set_title('Metrics vs k (n=4)')
# ax1.grid(True)
# ax1.set_xticks(k_values)
# ax1.legend()

# # Plot metrics vs n (k=4)
# n_values, precision_n, recall_n, hmean_n = zip(*n_data)
# ax2.plot(n_values, precision_n, marker='o', label='Precision')
# ax2.plot(n_values, recall_n, marker='s', label='Recall')
# ax2.plot(n_values, hmean_n, marker='^', label='H-mean')
# ax2.set_xlabel('n')
# ax2.set_ylabel('Score')
# ax2.set_title('Metrics vs n (k=4)')
# ax2.grid(True)
# ax2.set_xticks(n_values)
# ax2.legend()

# # Adjust layout
# plt.tight_layout()

# # Save as PDF
# plt.savefig('gss_hyperparameter_plots_with_metrics.pdf')
# print("Plot saved as 'gss_hyperparameter_plots_with_metrics.pdf'")