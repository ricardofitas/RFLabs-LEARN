"""RF Labs. teaching experiment: dependent rows do not create independent cases.

Run with Python 3.12+, NumPy and scikit-learn. All values are stipulated synthetic
teaching data, not specimen measurements or model-performance evidence. Groups
are assumed independent for illustration; five groups do not establish reliable
population inference. Duplication and covariance identities are exact checks.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import platform
import sys
import numpy as np
import sklearn
from sklearn.model_selection import GroupShuffleSplit, train_test_split

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "independence"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20261014

# START: dataset
case_effects = np.array([-1.2, -0.4, 0.0, 0.8, 1.4])
phase = np.linspace(0, 2 * np.pi, 100, endpoint=False)
within_case = 0.2 * np.sin(phase)
frames = case_effects[:, None] + within_case[None, :]
groups = np.repeat(np.arange(len(case_effects)), frames.shape[1])
flat = frames.ravel()
case_means = frames.mean(axis=1)

# START: standard_errors
row_sem = flat.std(ddof=1) / np.sqrt(flat.size)
case_sem = case_means.std(ddof=1) / np.sqrt(case_means.size)
duplicated = np.repeat(frames, 10, axis=1)
duplicate_row_sem = duplicated.ravel().std(ddof=1) / np.sqrt(duplicated.size)
duplicate_case_sem = duplicated.mean(axis=1).std(ddof=1) / np.sqrt(5)
np.testing.assert_allclose(case_means, case_effects, atol=1e-14)
np.testing.assert_allclose(duplicated.mean(axis=1), case_means, atol=1e-14)
np.testing.assert_allclose(duplicate_case_sem, case_sem, rtol=1e-14)
assert duplicate_row_sem < row_sem / 3

# START: unequal_groups
counts = np.array([20, 40, 60, 100, 200])
unequal = [effect + 0.2 * np.sin(np.linspace(0, 2 * np.pi, count, endpoint=False))
           for effect, count in zip(case_effects, counts)]
equal_case_mean = np.mean([x.mean() for x in unequal])
frame_weighted_mean = np.concatenate(unequal).mean()
np.testing.assert_allclose(equal_case_mean, case_effects.mean(), atol=1e-14)
np.testing.assert_allclose(frame_weighted_mean, np.average(case_effects, weights=counts))

# START: grouped_split
index = np.arange(flat.size)
train, test = next(GroupShuffleSplit(n_splits=1, test_size=0.4,
                                   random_state=SEED).split(index, groups=groups))
train2, validation2 = next(GroupShuffleSplit(n_splits=1, test_size=1 / 3,
                                            random_state=SEED + 1)
                          .split(train, groups=groups[train]))
train_final, validation = train[train2], train[validation2]
group_sets = [set(groups[x]) for x in (train_final, validation, test)]
assert not (group_sets[0] & group_sets[1] or group_sets[0] & group_sets[2]
            or group_sets[1] & group_sets[2])
assert set(np.concatenate([train_final, validation, test])) == set(index)
random_train, random_test = train_test_split(index, test_size=0.4, random_state=SEED)
leaked = sorted(set(groups[random_train]) & set(groups[random_test]))
assert leaked == list(range(5))

# START: bootstrap
rng = np.random.default_rng(SEED)
B = 20_000
case_indices = rng.integers(0, len(case_means), size=(B, len(case_means)))
case_bootstrap = case_means[case_indices].mean(axis=1)
row_indices = rng.integers(0, flat.size, size=(B, flat.size))
row_bootstrap = flat[row_indices].mean(axis=1)
case_interval = np.quantile(case_bootstrap, [0.025, 0.975])
row_interval = np.quantile(row_bootstrap, [0.025, 0.975])
assert np.ptp(case_interval) > 5 * np.ptp(row_interval)

# START: covariance
# Equal-size independent groups, common variance sigma2 and within-group rho.
# This identity concerns the variance of a mean, not a universal sample count.
G, m, rho, sigma2 = 5, 100, 0.8, 1.0
N = G * m
covariance = np.zeros((N, N))
for g in range(G):
    block = slice(g * m, (g + 1) * m)
    covariance[block, block] = sigma2 * rho
np.fill_diagonal(covariance, sigma2)
direct_variance = covariance.sum() / N**2
design_effect = 1 + (m - 1) * rho
formula_variance = sigma2 / N * design_effect
effective_n = N / design_effect
np.testing.assert_allclose(direct_variance, formula_variance, rtol=1e-14)
np.testing.assert_allclose(N / (1 + (m - 1)), G)

np.savez(OUT / "synthetic_groups.npz", frames=frames, groups=groups,
         case_bootstrap=case_bootstrap, row_bootstrap=row_bootstrap)
np.savetxt(OUT / "synthetic_rows.csv",
           np.column_stack((groups, np.tile(np.arange(100), 5), flat)),
           delimiter=",", header="case_id,frame_index,synthetic_value", comments="")
receipt = {
    "status": "PASS", "checkedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    "sourceSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "environment": {"python": sys.version, "numpy": np.__version__,
                    "sklearn": sklearn.__version__, "platform": platform.platform()},
    "seed": SEED, "bootstrap_draws": B,
    "evidence_class": "Stipulated synthetic teaching data; no actual measurements",
    "independence": "Five hypothetical independent cases; dependent frames within each",
    "results": {"rows": int(flat.size), "groups": 5, "mean": float(flat.mean()),
        "row_sem_iid_assumption": float(row_sem), "case_sem": float(case_sem),
        "duplicated_rows": int(duplicated.size), "duplicate_row_sem": float(duplicate_row_sem),
        "duplicate_case_sem": float(duplicate_case_sem), "unequal_counts": counts.tolist(),
        "equal_case_mean": float(equal_case_mean), "frame_weighted_mean": float(frame_weighted_mean),
        "train_groups": list(map(int, sorted(group_sets[0]))), "validation_groups": list(map(int, sorted(group_sets[1]))),
        "test_groups": list(map(int, sorted(group_sets[2]))), "random_split_overlapping_groups": list(map(int, leaked)),
        "case_percentile_interval": case_interval.tolist(), "row_percentile_interval": row_interval.tolist(),
        "design_effect_rho_08": float(design_effect), "variance_equivalent_n": float(effective_n),
        "direct_mean_variance": float(direct_variance)},
    "meaningful_checks": ["Duplication preserves case means and case SEM",
        "Unequal row weighting equals analytic weighted mean",
        "Group train/validation/test sets are disjoint and exhaustive",
        "Random row split shares all five case IDs",
        "Block covariance identity equals analytic design effect",
        "Case-level bootstrap has broader spread in this fixed example"],
    "limits": ["No model training, CPU/GPU performance or empirical ICC estimation",
        "Five synthetic groups cannot validate population confidence-interval coverage",
        "Percentile intervals show resampling mechanics, not a guaranteed inference procedure",
        "Grouped splitting requires the correct unit for the intended deployment",
        "Time dependence and higher-level batches may require additional blocking"]}
(OUT / "execution_receipt.json").write_text(json.dumps(receipt, indent=2))
print(json.dumps(receipt, indent=2))
