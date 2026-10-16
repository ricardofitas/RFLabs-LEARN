# Step 1
import numpy as np
from demo_visuals import paired_table, paired_plot
baseline = np.array([0.110, 0.170, 0.140, 0.190, 0.130])
candidate = np.array([0.095, 0.150, 0.125, 0.175, 0.120])
paired_table(baseline, candidate)

# Step 2
difference = candidate - baseline
print("Differences:", difference)
print(f"Means: {baseline.mean():.3f} → {candidate.mean():.3f}")
print(f"Mean difference: {difference.mean():+.3f}")
paired_plot(baseline, candidate)
print("Complete: inspect assets/lesson and animations in the file browser.")
