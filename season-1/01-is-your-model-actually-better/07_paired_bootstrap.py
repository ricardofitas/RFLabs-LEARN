# Step 1
from lesson_setup import *
pair_selection(baseline, candidate)

# Step 2
boot = bootstrap((candidate, baseline), mean_difference,
    paired=True, method="percentile", n_resamples=20_000,
    rng=np.random.default_rng(20261013))
ci = (boot.confidence_interval.low, boot.confidence_interval.high)
print(f"Illustrative 95% interval: [{ci[0]:.3f}, {ci[1]:.3f}]")
bootstrap_movie(boot.bootstrap_distribution, ci)
print("Complete: inspect assets/lesson and animations in the file browser.")
