import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- INCREASED FONT SIZES GLOBALLY ---
plt.rcParams.update({
    'font.size': 16,          # General/default font size
    'axes.titlesize': 20,     # Subplot title font size (e.g., 'No teacher')
    'axes.labelsize': 18,     # X and Y axis label font size ('Cost, c', 'Payoff')
    'xtick.labelsize': 14,    # X-axis tick numbers/labels
    'ytick.labelsize': 14     # Y-axis tick numbers/labels
})
# -------------------------------------

def process_and_plot(ax, filename, title):
    """
    Reads the data, calculates averages, and plots the bar chart and scatter points.
    """
    # Check if file exists to prevent crash
    if not os.path.exists(filename):
        ax.text(0.5, 0.5, f"File {filename} not found", ha='center', va='center')
        ax.set_title(title)
        return

    # Read the file. Assuming whitespace separation. 
    # If it is comma-separated, change sep=r'\s+' to sep=','
    df = pd.read_csv(filename, sep=r'\s+', header=None, names=['cost', 'payoff'])

    # Group the data by 'cost' (x) and calculate the mean of 'Scaled payoff' (y)
    grouped = df.groupby('cost')
    means = grouped['payoff'].mean().reset_index()

    # Create categorical x positions (ensures evenly spaced bars regardless of x values)
    x_labels = means['cost'].astype(str)
    x_positions = np.arange(len(x_labels))

    # 1. Plot the average as the height of the bar (removed label)
    ax.bar(x_positions, means['payoff'], color='skyblue', edgecolor='black', 
           alpha=0.7)

    # 2. Plot all the individual values as scatter points on top
    # Map the original cost values to the new categorical x positions
    cost_to_pos = {cost: pos for pos, cost in zip(x_positions, means['cost'])}
    scatter_x = df['cost'].map(cost_to_pos)

    # Plot the scatter points (alpha adds slight transparency so overlapping points appear darker)
    ax.scatter(scatter_x, df['payoff'], color='red', zorder=3, s=25, 
               alpha=0.6)

    # Formatting the subplot
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Cost, c')
    ax.set_ylabel('Payoff')
    ax.set_title(title)
    
    # Fix the y-axis range from 0 to 1
    ax.set_ylim(0, 1)
    
    # Grid formatting
    ax.grid(axis='y', linestyle='--', alpha=0.5)

def main():
    # Create a figure with 1 row and 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    # Plot data for c0.out on the left
    process_and_plot(axes[0], 'c0.out', 'No teacher (N=100)')

    # Plot data for c1.out on the right
    process_and_plot(axes[1], 'c1.out', 'One teacher (N=100)')

    # Adjust layout so labels don't overlap
    plt.tight_layout()

    # Save the figure to a PDF file
    output_filename = 'output_charts.pdf'
    plt.savefig(output_filename, format='pdf', bbox_inches='tight')
    
    print(f"Plot successfully saved to {output_filename}")

if __name__ == "__main__":
    main()