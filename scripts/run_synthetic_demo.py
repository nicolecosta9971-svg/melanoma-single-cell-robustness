"""From the repository root: python3 -B scripts/run_synthetic_demo.py."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from melanoma_portfolio.demo import run

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, allow_nan=False))
