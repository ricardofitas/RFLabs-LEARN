# Step 1
# Run the standalone program from a terminal with:
# python worked_example.py
import runpy; runpy.run_path("worked_example.py")

# Step 2
from IPython.display import Image, display
from pathlib import Path
print(Path("assets/lesson/synthetic_case_errors.csv").read_text())
display(Image("assets/lesson/paired_errors.png", width=1150))
print("Complete: inspect assets/lesson and animations in the file browser.")
