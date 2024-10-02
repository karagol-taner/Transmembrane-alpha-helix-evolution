import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Example median values for  > Amino Acid changes
median_values = {
'W':    0,
'A':    0.908,
'C':    0.962,
'D':    0.993,
'E':    0.990,
'F':    0.500,
'G':    0.807,
'H':    0.967,
'I':    0.926,
'K':    0.995,
'L':    0.778,
'M':    0.934,
'N':    0.985,
'P':    0.990,
'Q':    0.988,
'R':    0.986,
'S':    0.862,
'T':    0.926,
'V':    0.889,
'Y':    0.760,

}

# Example Q1 and Q3 values
q1_values = {
'W':    0,
'A':    0.506,
'C':    0.730,
'D':    0.910,
'E':    0.875,
'F':    0.26,
'G':    0.342,
'H':    0.783,
'I':    0.602,
'K':    0.895,
'L':    0.354,
'M':    0.632,
'N':    0.861,
'P':    0.902,
'Q':    0.832,
'R':    0.808,
'S':    0.423,
'T':    0.561,
'V':    0.501,
'Y':    0.464,

}

q3_values = {
'W':    0,
'A':    0.988,
'C':    0.996,
'D':    0.999,
'E':    0.999,
'F':    0.743,
'G':    0.965,
'H':    0.993,
'I':    0.988,
'K':    1.00,
'L':    0.956,
'M':    0.990,
'N':    0.998,
'P':    0.998,
'Q':    0.999,
'R':    0.998,
'S':    0.979,
'T':    0.991,
'V':    0.984,
'Y':    0.921,

}

# First and second half groups
first_half = ['A', 'C', 'F', 'G', 'I', 'L', 'M', 'P', 'V', 'W']
second_half = ['D', 'E', 'H', 'K', 'N', 'Q', 'R', 'S', 'T', 'Y']

# Create a DataFrame for the bar plot
data = {
    'Amino Acid': list(median_values.keys()),
    'Median': list(median_values.values()),
    'Q1': list(q1_values.values()),
    'Q3': list(q3_values.values())
}
df = pd.DataFrame(data)


# Sort first_half and second_half by median values
df_first_half = df[df['Amino Acid'].isin(first_half)].sort_values('Median')
df_second_half = df[df['Amino Acid'].isin(second_half)].sort_values('Median')

# Combine the sorted halves
df_sorted = pd.concat([df_first_half, df_second_half])

# Calculate error bars as the range from Q1 to Q3
lower_error = df_sorted['Median'] - df_sorted['Q1']
upper_error = df_sorted['Q3'] - df_sorted['Median']
errors = [lower_error, upper_error]

# Normalize the median values to the range [0, 1] for colormap
norm = mcolors.Normalize(vmin=df_sorted['Median'].min(), vmax=df_sorted['Median'].max())
cmap = cm.get_cmap('coolwarm')

# Bar plot with error bars and color mapping
plt.figure(figsize=(12, 6))
x = np.arange(len(df_sorted['Amino Acid']))  # The label locations
width = 0.7  # The width of the bars

fig, ax = plt.subplots(figsize=(12, 6))

# Add shaded regions behind the bars for different background colors
ax.axvspan(-0.7, len(df_first_half), facecolor='lightyellow', alpha=0.5)  # Left side background (slightly yellow)
ax.axvspan(len(df_first_half) - 0.5, len(df_sorted) -0.3 , facecolor='lightblue', alpha=0.5)  # Right side background (slightly blue)


bars = ax.bar(x, df_sorted['Median'], width, yerr=errors, capsize=5,
              color=cmap(norm(df_sorted['Median'])), edgecolor='black')

# Add labels, title, and legend
ax.set_ylabel('Scores', fontweight='bold', fontsize=22, labelpad=13)
ax.set_title('W>amino acid substitutions', fontweight='bold', fontsize=26, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(df_sorted['Amino Acid'], fontweight='bold', fontsize=20)

# Create a second y-axis on the right
ax2 = ax.twinx()

# Set the ticks on the right y-axis to match those on the left y-axis
ax2.set_yticks(ax.get_yticks())


# Set the limits for both y-axes
ax.set_ylim(0, 1.05)  # Set left y-axis limit
ax2.set_ylim(0, 1.05)  # Set right y-axis limit

# Make both x and y ticks bold
ax.tick_params(axis='x', which='major', labelsize=20, width=1, length=6, labelcolor='black')
ax.tick_params(axis='y', which='major', labelsize=18, width=1, length=6, labelcolor='black')
ax2.tick_params(axis='y', which='major', labelsize=18, width=1, length=6, labelcolor='black')  # Adjust right y-axis ticks

# Ensure tick labels on both axes are bold
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')
for tick in ax.get_yticklabels():
    tick.set_fontweight('bold')
for tick in ax2.get_yticklabels():
    tick.set_fontweight('bold')



# Add a vertical line dividing the graph in half (at the boundary between two groups)
ax.axvline(len(df_first_half) - 0.5, color='black', linestyle='-', lw=1,
           ymin=-0.18, ymax=1, clip_on=False)

# Add nonpolar and polar labels centered below the respective groups
nonpolar_center = np.mean(x[:len(df_first_half)])  # Center of the first half
polar_center = np.mean(x[len(df_first_half):])     # Center of the second half

# Set margins on the x-axis to reduce space between first/last bars and the plot boundaries
ax.margins(x=0.00)  # Reduce the x-axis margins to bring bars closer to edges


ax.text(nonpolar_center, -0.15, 'Hydrophobic amino acids', ha='center', va='center', fontsize=20, fontweight='bold', transform=ax.get_xaxis_transform())
ax.text(polar_center, -0.15, 'Hydrophilic amino acids', ha='center', va='center', fontsize=20, fontweight='bold', transform=ax.get_xaxis_transform())

# Add "Synonymous" label for the bar with a median value of 0
for bar, label in zip(bars, df_sorted['Amino Acid']):
    if df_sorted[df_sorted['Amino Acid'] == label]['Median'].values[0] == 0:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + 0.05, '(Synonymous)',
                va='bottom', ha='center', rotation=90, color='black', fontsize=15, fontweight='bold', fontstyle='italic')



plt.tight_layout()
plt.savefig('W_amino_acid_changes_sorted.svg', format='svg')
plt.show()

