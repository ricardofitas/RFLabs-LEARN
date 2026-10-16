# Step 1
from lesson_setup import *
boot = bootstrap((candidate, baseline), mean_difference,
    paired=True, method="percentile", n_resamples=20_000,
    rng=np.random.default_rng(20261013))
ci = (boot.confidence_interval.low, boot.confidence_interval.high)
bootstrap_movie(boot.bootstrap_distribution, ci)

# Step 2
# Separate experiment: independent Uniform(-1, 1) observations.
# Standardised sample means; n increases from 1 to 100.
# More independent observations ≠ more bootstrap repeats.
clt_movie()
print("Complete: inspect assets/lesson and animations in the file browser.")
