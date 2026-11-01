from pathlib import Path
import contextlib, io, runpy
with contextlib.redirect_stdout(io.StringIO()):
    _state = runpy.run_path(str(Path(__file__).with_name("independent_units.py")))
globals().update({k: v for k, v in _state.items() if not k.startswith("__")})
from lesson_visuals import *
