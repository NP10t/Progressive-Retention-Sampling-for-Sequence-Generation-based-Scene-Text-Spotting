import matplotlib.pyplot as plt

# Data
epochs = [0, 5, 10, 15, 20]
vanilla_sampling = [82.4, 79.4, 71.4, 59.9, 46.9]
gradual_subsequence_sampling = [82.4, 83.1, 83.5, 83.4, 83.5]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(epochs, vanilla_sampling, marker='o', label='Conventional Sampling', color='C1')  # Changed color to C1 (typically orange)
plt.plot(epochs, gradual_subsequence_sampling, marker='s', label='Progressive Retention Sampling (ours)', color='C0')  # Changed color to C0 (typically blue)

# Customize the plot
plt.xlabel('Epochs Applying Sampling')
plt.ylabel('H-mean')
# plt.title('Comparison of Progressive Retention Sampling (ours) with Conventional Sampling Across Epochs')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Set x-axis ticks to match the epoch values
plt.xticks(epochs)

# Add text to explain the starting point
plt.text(0, 83, 'Starting from a checkpoint', fontsize=9, verticalalignment='bottom')

# Optionally, add value labels on the points
for i, v in enumerate(vanilla_sampling):
    plt.text(epochs[i], v, f'{v}', ha='left', va='bottom')
for i, v in enumerate(gradual_subsequence_sampling):
    plt.text(epochs[i], v, f'{v}', ha='right', va='top')

# Save the plot as a PDF
plt.savefig('sampling_methods_comparison.pdf', bbox_inches='tight')
print("Plot saved as 'sampling_methods_comparison.pdf'")