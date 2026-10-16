"""VID-LEARN-001. Synthetic teaching data, not research results."""
from pathlib import Path
import itertools, json, hashlib, platform
import numpy as np
import scipy
from scipy.stats import bootstrap, permutation_test
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = Path(__file__).parent / "assets/lesson"
OUT.mkdir(parents=True, exist_ok=True)
baseline = np.array([0.110, 0.170, 0.140, 0.190, 0.130])
candidate = np.array([0.095, 0.150, 0.125, 0.175, 0.120])
difference = candidate - baseline
def mean_difference(x, y, axis=-1):
    return np.mean(x - y, axis=axis)
boot = bootstrap((candidate, baseline), mean_difference, paired=True,
                 method="percentile", n_resamples=20000,
                 rng=np.random.default_rng(20261013))
test = permutation_test((candidate, baseline), mean_difference,
                        permutation_type="samples", alternative="two-sided",
                        n_resamples=np.inf, vectorized=True)
signs = np.array(list(itertools.product([-1, 1], repeat=len(difference))))
null = (signs * difference).mean(axis=1)
p_enumerated = min(1.0, 2 * min(np.mean(null <= difference.mean()+1e-12),
                              np.mean(null >= difference.mean()-1e-12)))
assert test.null_distribution.size == 32
assert np.isclose(test.pvalue, 0.0625) and np.isclose(p_enumerated, test.pvalue)
assert np.isclose(baseline.mean(), 0.148) and np.isclose(candidate.mean(), 0.133)
assert np.isclose(difference.mean(), -0.015)
assert boot.confidence_interval.high < 0
# Construct 100 dependent frames per specimen. They are NOT 500 independent cases.
phase = np.linspace(0, 1, 100, endpoint=False)
shape = np.sin(2*np.pi*phase) + .5*np.cos(4*np.pi*phase)
shape /= np.sqrt(np.mean(shape**2))
baseline_residuals = baseline[:, None] * shape
candidate_residuals = candidate[:, None] * shape
assert np.allclose(np.sqrt(np.mean(baseline_residuals**2, axis=1)), baseline)
assert np.allclose(np.sqrt(np.mean(candidate_residuals**2, axis=1)), candidate)
replicated = np.repeat(candidate_residuals, 10, axis=1)
assert replicated.shape[0] == 5  # more frames do not create new specimens
assert np.allclose(np.sqrt(np.mean(replicated**2, axis=1)), candidate)
np.savetxt(OUT/"synthetic_case_errors.csv", np.c_[np.arange(1,6), baseline, candidate, difference],
           delimiter=",", header="synthetic_case,baseline_rmse,candidate_rmse,difference",
           comments="", fmt="%.6f")
np.savez(OUT/"synthetic_frames.npz", phase=phase,
         baseline_residuals=baseline_residuals, candidate_residuals=candidate_residuals)
palette={"bg":"#ffffff","panel":"#f6f9fb","ink":"#17202a","muted":"#51616f","blue":"#0e7490","gold":"#fb7185","line":"#d9e2ec"}
plt.rcParams.update({"figure.facecolor":palette["bg"],"axes.facecolor":palette["panel"],
"axes.edgecolor":palette["muted"],"axes.labelcolor":palette["ink"],
"text.color":palette["ink"],"xtick.color":palette["muted"],"ytick.color":palette["muted"],
"font.size":17,"savefig.facecolor":palette["bg"]})
fig,ax=plt.subplots(figsize=(14,7))
for i,(a,b) in enumerate(zip(baseline,candidate),1):
    ax.plot([0,1],[a,b],color=palette["muted"],alpha=.7)
    ax.scatter([0,1],[a,b],color=[palette["gold"],palette["blue"]],s=100,zorder=3)
    ax.text(1.03,b,f"Case {i}",va="center",fontsize=14)
ax.set_xticks([0,1],["Baseline","Candidate"]);ax.set_xlim(-.2,1.4)
ax.set_ylabel("RMSE [arbitrary teaching units]")
ax.set_title("Five paired cases - synthetic teaching data")
ax.text(.02,.03,"Mean difference = -0.015 | 5 independent units",transform=ax.transAxes,color=palette["blue"])
fig.tight_layout();fig.savefig(OUT/"paired_errors.png",dpi=160);fig.savefig(OUT/"paired_errors.svg");plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(16,7))
axes[0].hist(boot.bootstrap_distribution,bins=np.linspace(-.021,-.009,25),color=palette["blue"])
axes[0].axvline(0,color=palette["gold"],linestyle="--");axes[0].set_xlim(-.024,.003)
axes[0].set_title("Percentile bootstrap | same five cases")
axes[0].set_xlabel("Candidate minus baseline RMSE")
axes[0].set_ylabel("Resamples");axes[0].text(.03,.94,"Illustrative interval; small-n limitations",transform=axes[0].transAxes,fontsize=13)
axes[1].hist(null,bins=np.linspace(-.016,.016,18),color=palette["gold"])
axes[1].axvline(difference.mean(),color=palette["blue"],linestyle="--")
axes[1].set_title("Exact paired sign flips | 32 assignments")
axes[1].set_xlabel("Mean signed difference");axes[1].set_ylabel("Assignments")
axes[1].text(.05,.94,"Two-sided p = 0.0625",transform=axes[1].transAxes,fontsize=15)
fig.suptitle("Synthetic example - no evidence about a real model")
fig.tight_layout();fig.savefig(OUT/"uncertainty.png",dpi=160);fig.savefig(OUT/"uncertainty.svg");plt.close(fig)
receipt={"ticket":"VID-LEARN-001","data_class":"synthetic teaching data",
"executed_at_utc":__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
"environment":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,"matplotlib":matplotlib.__version__},
"cases":5,"frames_per_case":100,"baseline_mean":float(baseline.mean()),
"candidate_mean":float(candidate.mean()),"mean_difference":float(difference.mean()),
"bootstrap":{"method":"paired percentile","resamples":20000,"seed":20261013,
"interval":[float(boot.confidence_interval.low),float(boot.confidence_interval.high)],
"limitation":"five cases; interval is an illustrative resampling calculation, not population validation"},
"permutation":{"assignments":32,"two_sided_p":float(test.pvalue),
"assumption":"model-label exchangeability within independent cases under the null"},
"checks":{"scipy_matches_enumeration":"PASS","case_rmse_reconstruction":"PASS","frame_replication_not_new_cases":"PASS"},
"source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/"execution_receipt.json").write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
fig,ax=plt.subplots(figsize=(16,5.8))
ax.hist(boot.bootstrap_distribution,bins=np.linspace(-.021,-.009,25),color=palette['blue'])
ax.axvline(0,color=palette['gold'],linestyle='--')
ax.set_xlim(-.024,.003)
ax.set_xlabel('Candidate minus baseline RMSE',fontsize=23)
ax.set_ylabel('Resamples',fontsize=23)
ax.tick_params(labelsize=20)
ax.set_title('Paired percentile bootstrap: same five cases',fontsize=25)
fig.tight_layout();fig.savefig(OUT/'bootstrap_single.png',dpi=160);plt.close(fig)


# Also expose the generated outputs in the JupyterLab file browser.
from demo_visuals import paired_table
paired_table(baseline, candidate)
import shutil
for filename in ["paired_errors.png", "uncertainty.png"]:
    shutil.copy2(OUT / filename, Path(__file__).parent / filename)
