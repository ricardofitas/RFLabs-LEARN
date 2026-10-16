# Step 1
from lesson_setup import *
import itertools
signs = np.array(list(itertools.product([-1, 1], repeat=5)))
null = (signs * difference).mean(axis=1)
assert len(null) == 32
exact_movie(difference)

# Step 2
test = permutation_test((candidate, baseline), mean_difference,
    permutation_type="samples", alternative="two-sided",
    n_resamples=np.inf, vectorized=True)
assert test.null_distribution.size == 32
assert np.isclose(test.pvalue, 0.0625)
print(f"Exact two-sided p = {test.pvalue:.4f}")
exact_movie(difference)
print("Complete: inspect assets/lesson and animations in the file browser.")
