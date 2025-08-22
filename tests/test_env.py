import os
from pathlib import Path

def test_sumo_smoke():
    assert "SUMO_HOME" in os.environ
    root = Path(__file__).resolve().parents[1]
    # Run einmal starten, erzeugt bei Bedarf routes + cfg
    import sys
    sys.path.append(str(root / "src"))
    import run  # type: ignore
    run.run(gui=False, steps=50)
