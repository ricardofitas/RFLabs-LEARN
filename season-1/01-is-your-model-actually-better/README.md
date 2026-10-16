# Is Your Model Actually Better?

Companion materials for **Season 1, episode 01 — Is Your Model Actually Better?**
by [Ricardo Fitas](https://www.youtube.com/@ricardofitas).

The motivating example is a tensile test: a machine pulls a metal bar and we
compare two models that predict its elongation. The numerical scores below are
**synthetic teaching data**, expressed in arbitrary teaching units. They are not
experimental metal-test results and no predictive model is trained here.

This folder contains the executable Python scripts and notebooks used in the
video. The `materials/` folder contains the transcript, English SRT/VTT captions,
thumbnail and input scores. `assets/lesson/` contains reproducible results and
figures; `animations/` contains computed demonstrations. Running the scripts
regenerates these teaching outputs.

YouTube: awaiting channel verification. The initial upload was rejected by YouTube's 15-minute limit; this lesson is 16:06. The approved video will be re-uploaded after the long-video feature is enabled.

[Back to the Season 1 episode list](../../README.md#season-1).

## Quick start

Use Python 3.12 or newer. Open a terminal in this folder.

Windows:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python worked_example.py
```

macOS / Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python worked_example.py
```

The complete statistical calculation and static figures require only the Python
dependencies. To generate the animated demonstrations, also install **FFmpeg**
and ensure `ffmpeg` is available on your PATH. No service account or API key is
required.

Run every demonstration with the same environment:

```powershell
# Windows
.venv\Scripts\python run_all.py
```

```sh
# macOS / Linux
.venv/bin/python run_all.py
```

The commands in the table below use `python` for brevity. Substitute the
virtual environment executable above, or activate that environment first.

For JupyterLab, install `jupyterlab` into the same environment, run
`python -m jupyterlab` from this folder, then open a script or notebook. In its
terminal, run the same commands shown below. JupyterLab is optional; the scripts
also run in any ordinary terminal or Python IDE.

## Scripts in video order

| Scene | Command | What it produces |
|---|---|---|
| 05 | `python 05_paired_scores.py` | Paired table and score animation |
| 06 | `python 06_case_metric.py` | Case-average versus pooled RMSE |
| 07 | `python 07_paired_bootstrap.py` | Pair selection and bootstrap animation |
| 08 | `python 08_resampling_and_clt.py` | Resampling stability and a separate CLT illustration |
| 09 | `python 09_exact_sign_flips.py` | All 32 sign assignments |
| 10 | `python 10_interval_and_test.py` | Interval and exact-test comparison |
| 11 | `python 11_dependent_frames.py` | Why repeated frames do not add specimens |
| 14 | `python worked_example.py` | Complete calculation, assertions, CSV, arrays and static figures |

`lesson_setup.py` defines shared inputs; `demo_visuals.py` renders the plots.
Notebooks contain equivalent steps for interactive use. Run commands from this
folder so imports and generated-file links resolve consistently.

## Expected results

| Quantity | Result |
|---|---:|
| Independent synthetic cases | 5 |
| Mean baseline case RMSE | 0.148 |
| Mean candidate case RMSE | 0.133 |
| Mean paired difference, candidate minus baseline | -0.015 |
| Paired percentile bootstrap interval | [-0.018, -0.012] |
| Exact sign assignments | 32 |
| Two-sided sign-flip p-value | 0.0625 |

The bootstrap uses 20,000 resamples and seed 20261013. The assertions verify
pairing arithmetic, agreement with explicit sign enumeration, reconstruction of
case-level RMSE from frame residuals, and invariance to duplicating frames.

Outputs appear in `assets/lesson/`, `animations/` and this folder. The execution
receipt records the actual dependency versions and calculation results.

## Interpretation and adaptation

Five cases cannot establish reliable population coverage or deployment quality.
The sign-flip calculation requires label exchangeability within independent
pairs under its null. Additional bootstrap repetitions improve computational
precision; they do not create new independent test specimens. The CLT animation
is a separate simulation from a known uniform population.

Replace the synthetic case scores with your own protected evaluation, keep
matching case IDs together, and reconsider independence, weighting and the null
assumptions. Do not tune your candidate using the final test set.

## References

- [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)
- [SciPy permutation_test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html)
- [NumPy mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)

Prepared for the video by Ricardo Fitas. Dependency licences remain with their
respective authors. No licence for redistribution of the narration is included.
