# How Much Independent Data Do You Have?

Companion materials for LEARN, Season 1, Episode 2.

Run the executed example:

```bash
python -m pip install -r requirements.txt
python independent_units.py
```

The program writes `assets/independence/execution_receipt.json`, the synthetic
arrays and a CSV table. Its assertions check duplication, case-level summaries,
row and case weighting, grouped partitions and a specified covariance identity.

Follow the lesson by inspecting the blocks marked `dataset`, `standard_errors`,
`unequal_groups`, `grouped_split`, `bootstrap` and `covariance`. Run the whole
program before interpreting individual blocks: they share the same arrays and
fixed seed. The notebook provides the same calculation in executable cells.

These are stipulated synthetic teaching data: five hypothetical independent
cases, each with 100 related frames. No real specimens, trained predictor,
empirical correlation estimate or validated confidence-interval coverage is
claimed. The covariance example is a separate conditional model.

Verified environment: Python 3.12, NumPy 2.3.5, scikit-learn 1.8.0.

Video status: revised private review; publication requires the owner's final
acceptance. The numerical example is available independently of the video.

## JupyterLab walkthrough

The revised video executes this episode's code in real JupyterLab. Open the
[numbered demonstration notebooks](jupyter/README.md) to follow the same sequence
of calculations and generated plots. Each notebook can run from a fresh kernel;
its setup imports the unchanged `independent_units.py` program and fixed seed.
The saved notebook outputs are the outputs recorded in the video.
