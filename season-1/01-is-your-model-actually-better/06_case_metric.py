# Step 1
from lesson_setup import *
paired_plot(baseline, candidate)

# Step 2
case_average = candidate.mean()
pooled_rmse = np.sqrt(np.mean(candidate**2))
print(f"Equal-case mean RMSE: {case_average:.3f}")
print(f"Pooled RMSE, equal frame counts: {pooled_rmse:.3f}")
# Different estimands, even before unequal sequence lengths.
paired_plot(baseline, candidate)
print("Complete: inspect assets/lesson and animations in the file browser.")
