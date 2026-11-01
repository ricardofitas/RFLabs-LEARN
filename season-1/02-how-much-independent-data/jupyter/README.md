# LEARN 002 — JupyterLab demonstrations

These notebooks contain the code used in the revised video **How much independent
data do you really have?** Their saved outputs were produced by a real Python
kernel in JupyterLab. The video records the typing or inspection of code, its
execution, its printed results, the resulting Matplotlib plot, and a return to
the relevant calculation.

Install the dependencies and open this directory in JupyterLab:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open any numbered notebook and choose **Run → Run All Cells**. The first cell
imports `lesson_setup`, which executes the unchanged episode program
`independent_units.py` with its fixed seed. The next cell performs the calculation
shown in that part of the lesson. The last cell plots its actual arrays with
`lesson_visuals.py`. Each notebook can be run independently in a fresh kernel.

| Notebook | Calculation |
| --- | --- |
| 03_dataset | Construct the five cases and retain each row's case identity |
| 04_executed_values | Check the specified case means and the overall mean |
| 05_standard_errors | Compare row and case standard-error assumptions |
| 06_duplicate_rows | Duplicate rows without creating independent cases |
| 08_covariance_model | Check a separate, specified covariance model |
| 09_unequal_groups | Compare equal-case and row-count weighting |
| 10_random_row_split | Identify case overlap after a random row split |
| 11_grouped_partitions | Verify disjoint train, validation and test cases |
| 13_bootstrap_units | Resample whole cases or individual rows |

The data are synthetic teaching examples. Separate physical objects are not
automatically independent: the sampling design, shared conditions and target
of inference determine which units can support the intended conclusion.

The numerical code and seed belong to this episode. LEARN 001 is only the
reference for the JupyterLab recording and teaching method.
