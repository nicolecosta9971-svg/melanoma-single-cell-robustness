"""Run the invented-count analysis without scientific dependencies or input files."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from melanoma_portfolio.bootstrap import DEFAULT_DRAWS, DEFAULT_SEED, MAX_DRAWS, run


def main() -> None:
    parser = argparse.ArgumentParser(description="Patient-level bootstrap and sensitivity checks on invented data")
    parser.add_argument("--draws", type=int, default=DEFAULT_DRAWS,
                        help=f"number of bootstrap draws (2–{MAX_DRAWS}, default: %(default)s)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="random seed (default: %(default)s)")
    args = parser.parse_args()
    try:
        result = run(draws=args.draws, seed=args.seed)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
