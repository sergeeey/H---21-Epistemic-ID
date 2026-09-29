#!/usr/bin/env python3
"""One-command reproduction of the publicly shipped synthetic checks.

Reproduces:
  1. Mutual-information units check (nats vs bits) for p=0.64, q=0.95
  2. Action scores / sampling probabilities at the published top v1 condition
  3. Optional compact grid search for top discriminating conditions

Does NOT reproduce v4–v8 matched-channel searches. Those results are
reported in the preprint; the corresponding pipeline is not in this repository.

Usage:
    python scripts/reproduce.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "artifacts"))

from reduced_aif_v1 import (  # noqa: E402
    Condition,
    action_probabilities,
    binary_entropy,
    grid_search,
    mutual_information_state_cue,
)


def almost(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def check_mi() -> None:
    p, q = 0.64, 0.95
    py = p * q + (1.0 - p) * (1.0 - q)
    h_y = binary_entropy(py)
    h_yz = binary_entropy(q)
    ig = mutual_information_state_cue(p, q)
    ig_bits = ig / math.log(2.0)
    print("== MI units check (nats) ==")
    print(f"P(Y=L)              = {py:.6f}   expected 0.626")
    print(f"H(Y)                = {h_y:.6f}   ~ 0.6610 nats")
    print(f"H(Y|Z)=H(q)         = {h_yz:.6f}   ~ 0.1985 nats")
    print(f"I(Z;Y)              = {ig:.6f}   ~ 0.4625 nats")
    print(f"H(Y) if misread bits= {h_y / math.log(2):.6f}   ~ 0.953 (bits, not nats)")
    print(f"I(Z;Y) in bits      = {ig_bits:.6f}")
    assert almost(py, 0.626, 1e-12)
    assert almost(ig, 0.4625, 5e-4)
    print("PASS: nats formula matches the preprint verification note.\n")


def check_top_condition() -> None:
    # First row of artifacts/reduced_aif_v1_top_conditions.csv
    cond = Condition(p_left=0.64, cue_reliability=0.95, sample_cost=0.40, safe_reward=0.55)
    pa, pb, sa, sb, ig = action_probabilities(cond, beta=8.0, alpha_epi=1.0)
    print("== Top published v1 condition (p=0.64, q=0.95, c=0.40, β=8, α=1) ==")
    print(f"I(Z;Y)              = {ig:.6f}")
    print(f"AIF SAMPLE score    = {sa[3]:.6f}   expected ~ 1.0125")
    print(f"BRL SAMPLE score    = {sb[3]:.6f}   expected ~ 0.5500")
    print(f"P_AIF(SAMPLE)       = {pa[3]:.6f}   expected ~ 0.9252")
    print(f"P_BRL(SAMPLE)       = {pb[3]:.6f}   expected ~ 0.2340")
    assert almost(sa[3], 1.012535, 5e-4)
    assert almost(sb[3], 0.55, 5e-4)
    assert almost(float(pa[3]), 0.925154, 5e-4)
    assert almost(float(pb[3]), 0.234020, 5e-4)
    print("PASS: recomputed scores match the published top-condition CSV.\n")


def check_compact_grid() -> None:
    print("== Compact discrimination grid (may take a few seconds) ==")
    rows = grid_search(
        p_grid=np.linspace(0.50, 0.95, 19),
        q_grid=np.linspace(0.55, 0.95, 17),
        cost_grid=np.linspace(0.00, 0.40, 17),
        beta=8.0,
        alpha_epi=1.0,
        safe_reward=0.55,
    )
    best = rows[0]
    print(
        f"Best compact-grid JS = {best['js_divergence']:.4f} | "
        f"p={best['prior_p_left']:.2f} q={best['cue_reliability']:.2f} "
        f"c={best['sample_cost']:.2f} | "
        f"Psample AIF={best['P_AIF_SAMPLE']:.3f} BRL={best['P_BRL_SAMPLE']:.3f}"
    )
    print("Top 5 compact-grid conditions:")
    for i, r in enumerate(rows[:5], 1):
        print(
            f"  {i}. JS={r['js_divergence']:.4f}  "
            f"p={r['prior_p_left']:.2f} q={r['cue_reliability']:.2f} "
            f"c={r['sample_cost']:.2f}"
        )
    assert best["P_AIF_SAMPLE"] > best["P_BRL_SAMPLE"]
    print(
        "PASS: reduced exact-MI controller samples more than reward-only control in the top cell.\n"
    )


def main() -> None:
    print("Shipped reproduction: v1 reduced AIF vs instrumental Bayes only.")
    print("v4–v8 matched-channel results are in the preprint, not in this script.\n")
    check_mi()
    check_top_condition()
    check_compact_grid()
    from nelson2010 import assert_paper_claims, F, G

    assert_paper_claims()
    print("== Nelson 2010 E3C1 independent check ==")
    print(
        f"F: Acc={F.expected_accuracy():.4f} PG={F.probability_gain():.4f} I={F.mutual_information_nats():.4f} nats"
    )
    print(
        f"G: Acc={G.expected_accuracy():.4f} PG={G.probability_gain():.4f} I={G.mutual_information_nats():.4f} nats"
    )
    print("PASS: Nelson Condition 1 PG/accuracy tied; I(F) > I(G).\n")
    print("ALL SHIPPED CHECKS PASSED.")
    print("Do not use any of these synthetic rates to choose human sample size.")


if __name__ == "__main__":
    main()
