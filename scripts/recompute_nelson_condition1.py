#!/usr/bin/env python3
"""Print the independent Nelson 2010 Experiment 3 Condition 1 recalculation."""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "artifacts"))

from nelson2010 import F, G, assert_paper_claims, condition1_table


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    p = k / n
    den = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return center - half, center + half


def main() -> None:
    assert_paper_claims()
    rows = condition1_table()
    out = ROOT / "docs" / "protocol_v2_audit" / "nelson_2010_condition1_recalculation.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("Nelson et al. 2010  Experiment 3 Condition 1  (independent recalculation)")
    print("Units: nats (natural log). Probability gain as defined by Baron / Nelson.")
    for r in rows:
        print(
            f"  {r['channel']}: prior={r['prior']:.2f}  "
            f"Acc={r['bayes_optimal_accuracy']:.4f}  "
            f"PG={r['probability_gain']:.4f}  "
            f"I={r['mutual_information_nats']:.4f} nats"
        )
    lo, hi = wilson_ci(12, 22)
    print("Human preference for higher-IG feature F: 12/22 = 0.545")
    print(f"Approximate 95% Wilson CI: [{lo:.3f}, {hi:.3f}]")
    print("This is not a precise original-paper inference; it is a descriptive interval.")
    print("wrote", out)
    print("PASS: PG tied at 0.25; Acc tied at 0.75; I(F) > I(G).")


if __name__ == "__main__":
    main()
