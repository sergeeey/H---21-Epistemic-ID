#!/usr/bin/env python3
"""EQR on matched asymmetric channels.

Probe algebra: (p, a, b, cost). A matched pair holds prior, mean accuracy,
and instrumental sample value fixed, and lets exact I(Z;Y) differ.

Coarse curiosity, which sees only (p, q_bar), then predicts Delta P = 0
on a cost-matched pair. Exact-MI does not.

This does not reproduce preprint Table 3. It searches its own pairs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "artifacts"))

from asymmetric_channel import (  # noqa: E402
    Channel,
    cost_match,
    curiosity_bonus,
    valid_channel,
)
from reduced_aif_v1 import mutual_information_state_cue  # noqa: E402

OUT = ROOT / "artifacts" / "eqr_asymmetric_audit.json"


def search_pairs(min_delta_mi: float = 0.05) -> list[dict]:
    rows = []
    for p in (0.70, 0.80):
        for q_bar in np.round(np.arange(0.70, 0.91, 0.02), 5):
            channels = []
            for a in np.round(np.arange(0.55, 0.98, 0.01), 5):
                ch = valid_channel(float(p), float(a), float(q_bar))
                if ch is None:
                    continue
                channels.append(ch)
            if len(channels) < 2:
                continue
            gross = [c.gross_classification_value() for c in channels]
            target = min(gross)
            # Pair the lowest-MI and highest-MI channels at this (p, q_bar).
            order = sorted(
                range(len(channels)), key=lambda i: channels[i].mutual_information_nats()
            )
            lo, hi = channels[order[0]], channels[order[-1]]
            dmi = hi.mutual_information_nats() - lo.mutual_information_nats()
            if dmi < min_delta_mi:
                continue
            left, right = cost_match(lo, target), cost_match(hi, target)
            if left.sample_cost < -1e-9 or right.sample_cost < -1e-9:
                continue
            rows.append(_pair_record(left, right))
    rows.sort(key=lambda r: r["delta_mi_nats"], reverse=True)
    return rows


def _delta_p(
    lo: Channel, hi: Channel, bonus_lo: float, bonus_hi: float, beta: float = 8.0
) -> float:
    return float(hi.policy(bonus_hi, beta)[3] - lo.policy(bonus_lo, beta)[3])


def _pair_record(lo: Channel, hi: Channel) -> dict:
    beta = 8.0
    alpha = 1.0
    kappa, gamma = 1.0, 2.0
    i_lo, i_hi = lo.mutual_information_nats(), hi.mutual_information_nats()
    amb_lo, amb_hi = lo.ambiguity_nats(), hi.ambiguity_nats()
    bonus_lo = curiosity_bonus(lo.p_left, lo.mean_accuracy(), kappa, gamma)
    bonus_hi = curiosity_bonus(hi.p_left, hi.mean_accuracy(), kappa, gamma)
    p_cur_lo = lo.policy(bonus_lo, beta)[3]
    p_cur_hi = hi.policy(bonus_hi, beta)[3]
    p_mi_lo = lo.policy(alpha * i_lo, beta)[3]
    p_mi_hi = hi.policy(alpha * i_hi, beta)[3]
    # I = H(Y) - H(Y|Z), so an extra -H(Y|Z) double-counts ambiguity.
    delta_p_mi = _delta_p(lo, hi, alpha * i_lo, alpha * i_hi)
    delta_p_ambiguity_only = _delta_p(lo, hi, -amb_lo, -amb_hi)
    delta_p_I_minus_ambiguity = _delta_p(lo, hi, i_lo - amb_lo, i_hi - amb_hi)
    return {
        "p": lo.p_left,
        "q_bar_lo": lo.mean_accuracy(),
        "q_bar_hi": hi.mean_accuracy(),
        "a_lo": lo.sensitivity,
        "b_lo": lo.specificity,
        "a_hi": hi.sensitivity,
        "b_hi": hi.specificity,
        "cost_lo": lo.sample_cost,
        "cost_hi": hi.sample_cost,
        "I_lo": lo.mutual_information_nats(),
        "I_hi": hi.mutual_information_nats(),
        "delta_mi_nats": i_hi - i_lo,
        "delta_H_Y_nats": (i_hi + amb_hi) - (i_lo + amb_lo),
        "ambiguity_lo": amb_lo,
        "ambiguity_hi": amb_hi,
        "delta_ambiguity_nats": amb_hi - amb_lo,
        "share_of_delta_I_from_ambiguity": (amb_lo - amb_hi) / (i_hi - i_lo)
        if abs(i_hi - i_lo) > 1e-12
        else None,
        "delta_P_ambiguity_only": delta_p_ambiguity_only,
        "delta_P_I_minus_ambiguity": delta_p_I_minus_ambiguity,
        "delta_P_exact_mi_signed": delta_p_mi,
        "V_instr_lo": lo.instrumental_sample_value(),
        "V_instr_hi": hi.instrumental_sample_value(),
        "delta_P_exact_mi": abs(p_mi_hi - p_mi_lo),
        "delta_P_curiosity_k1_g2": abs(p_cur_hi - p_cur_lo),
        "P_exact_mi_lo": p_mi_lo,
        "P_exact_mi_hi": p_mi_hi,
    }


def search_ambiguity_matched(
    amb_tol: float = 0.005, q_tol: float = 0.005, min_delta_mi: float = 0.05
) -> list[dict]:
    """Pairs with the same prior, nearly the same q_bar, and nearly the same H(Y|Z)."""
    rows = []
    for p in (0.70, 0.80):
        channels = []
        for a in np.round(np.arange(0.55, 0.98, 0.02), 5):
            for b in np.round(np.arange(0.55, 0.98, 0.02), 5):
                ch = Channel(float(p), float(a), float(b))
                py = ch.p_y_left()
                if py <= 1e-6 or py >= 1.0 - 1e-6:
                    continue
                channels.append(ch)
        for i, left0 in enumerate(channels):
            for right0 in channels[i + 1 :]:
                if abs(left0.mean_accuracy() - right0.mean_accuracy()) > q_tol:
                    continue
                if abs(left0.ambiguity_nats() - right0.ambiguity_nats()) > amb_tol:
                    continue
                lo, hi = left0, right0
                if hi.mutual_information_nats() < lo.mutual_information_nats():
                    lo, hi = hi, lo
                if hi.mutual_information_nats() - lo.mutual_information_nats() < min_delta_mi:
                    continue
                target = min(lo.gross_classification_value(), hi.gross_classification_value())
                left, right = cost_match(lo, target), cost_match(hi, target)
                if left.sample_cost < -1e-8 or right.sample_cost < -1e-8:
                    continue
                rows.append(_pair_record(left, right))
    rows.sort(key=lambda r: r["delta_mi_nats"], reverse=True)
    return rows


def symmetric_reduction_ok() -> dict:
    p, q = 0.64, 0.95
    ch = Channel(p, q, q, sample_cost=0.40)
    from reduced_aif_v1 import sample_instrumental_value

    return {
        "I_asym": ch.mutual_information_nats(),
        "I_sym": mutual_information_state_cue(p, q),
        "V_asym": ch.instrumental_sample_value(),
        "V_sym": sample_instrumental_value(p, q, 0.40),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    pairs = search_pairs()
    matched = search_ambiguity_matched()
    red = symmetric_reduction_ok()
    sign_conflict = sum(
        1 for r in pairs if r["delta_P_exact_mi_signed"] * r["delta_P_ambiguity_only"] < 0
    )
    report = {
        "probe_algebra": "asymmetric (a, b) with cost-matched instrumental value",
        "n_pairs": len(pairs),
        "symmetric_reduction": red,
        "ambiguity_gate_unmatched": {
            "n_pairs": len(pairs),
            "n_sign_conflict_exact_mi_vs_ambiguity_only": sign_conflict,
            "max_abs_delta_ambiguity": max(abs(r["delta_ambiguity_nats"]) for r in pairs),
            "min_delta_P_exact_mi": min(r["delta_P_exact_mi"] for r in pairs),
        },
        "ambiguity_matched_pairs": {
            "tolerance_nats": 0.005,
            "q_bar_tolerance": 0.005,
            "n_pairs": len(matched),
            "top": matched[:5],
            "min_delta_P_exact_mi": min((r["delta_P_exact_mi"] for r in matched), default=None),
            "max_abs_delta_P_curiosity": max(
                (r["delta_P_curiosity_k1_g2"] for r in matched), default=None
            ),
        },
        "top_pairs": pairs[:8],
        "curiosity_sees_only_q_bar": True,
        "table3_status": "not reproduced; these pairs are a new search",
        "verdict": (
            "Ambiguity gate: when H(Y|Z) is matched within 0.005 nats, exact-MI "
            "still separates the pair and coarse curiosity stays near zero. "
            "The sampling contrast does not require a large ambiguity gap. "
            "On pairs that leave ambiguity free, an ambiguity-only score conflicts "
            "in sign with exact-MI on part of the set, so the term is real but "
            "not the whole contrast. Preprint Table 3 remains unverified."
        ),
        "note": (
            "I(Z;Y) already equals H(Y)-H(Y|Z). delta_P_ambiguity_only scores -H(Y|Z) "
            "alone. An extra -H(Y|Z) on top of I double-counts. "
            "Preprint Table 3 is not copied."
        ),
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("symmetric reduction", red)
    print("pairs found", len(pairs), "sign conflicts", sign_conflict)
    print("ambiguity-matched pairs", len(matched))
    if matched:
        m = matched[0]
        print(
            f"best ambiguity-matched dMI={m['delta_mi_nats']:.4f} "
            f"dAmb={m['delta_ambiguity_nats']:.4f} "
            f"dP_mi={m['delta_P_exact_mi']:.4f} "
            f"dP_cur={m['delta_P_curiosity_k1_g2']:.3e}"
        )
    if pairs:
        top = pairs[0]
        print(
            f"top pair p={top['p']} q~{top['q_bar_lo']:.3f} "
            f"dMI={top['delta_mi_nats']:.4f} "
            f"dP_mi={top['delta_P_exact_mi']:.4f} "
            f"dP_cur={top['delta_P_curiosity_k1_g2']:.3e} "
            f"dAmb={top['delta_ambiguity_nats']:.4f}"
        )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
