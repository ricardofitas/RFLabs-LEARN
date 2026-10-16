# Step 1
from lesson_setup import *
boot = bootstrap((candidate, baseline), mean_difference,
    paired=True, method="percentile", n_resamples=20_000,
    rng=np.random.default_rng(20261013))
ci = (boot.confidence_interval.low, boot.confidence_interval.high)
comparison_movie(boot.bootstrap_distribution, ci, difference)
print("Complete: inspect assets/lesson and animations in the file browser.")
