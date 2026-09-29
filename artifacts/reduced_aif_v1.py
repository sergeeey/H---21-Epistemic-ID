"""
Epistemic ID — reduced v1 simulation
Minimal discriminating experiment: reduced EFE-derived exact-MI controller
vs Bayesian reward-maximizing control.

The task is a one-step hidden-context decision problem.

Hidden state:
    Z in {L, R}, with prior P(Z=L)=p.

Actions at stage 0:
    SAFE      -> deterministic reward r_safe.
    COMMIT_L  -> reward r_win if Z=L else r_lose.
    COMMIT_R  -> reward r_win if Z=R else r_lose.
    SAMPLE    -> pay cost c, observe a noisy cue Y about Z, then commit optimally.

Cue model:
    P(Y=Z) = q.

Bayesian-RL / Bayes-optimal reward model:
    scores actions by expected instrumental reward only.

Reduced Active-Inference model:
    uses the expected-free-energy decomposition
        -G(pi) = expected log preference + expected information gain
    and, with log-preferences proportional to reward, scores SAMPLE as
        E[reward | SAMPLE] + alpha_epi * I(Z;Y).
    Other actions have zero epistemic term in this minimal task.

This is intentionally a small, exact discriminating model—not a claim that
all of Active Inference reduces to this task.
"""

from __future__ import annotations
import argparse
import csv
import math
from dataclasses import dataclass
from typing import Dict, Tuple, List
import numpy as np


ACTIONS = ("SAFE", "COMMIT_L", "COMMIT_R", "SAMPLE")


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log(p) + (1.0 - p) * math.log(1.0 - p))


def cue_probability(p: float, q: float, cue_l: bool) -> float:
    """P(Y=L) if cue_l else P(Y=R)."""
    if cue_l:
        return p * q + (1.0 - p) * (1.0 - q)
    return p * (1.0 - q) + (1.0 - p) * q


def posterior_p_left(p: float, q: float, cue_l: bool) -> float:
    """Bayes posterior P(Z=L | cue)."""
    if cue_l:
        num = p * q
        den = p * q + (1.0 - p) * (1.0 - q)
    else:
        num = p * (1.0 - q)
        den = p * (1.0 - q) + (1.0 - p) * q
    return num / den


def commit_values(p: float, r_win: float = 1.0, r_lose: float = 0.0) -> Tuple[float, float]:
    v_l = p * r_win + (1.0 - p) * r_lose
    v_r = (1.0 - p) * r_win + p * r_lose
    return v_l, v_r


def sample_instrumental_value(
    p: float, q: float, cost: float, r_win: float = 1.0, r_lose: float = 0.0
) -> float:
    """
    Expected reward if the agent samples a cue and then commits optimally.
    This includes the sampling cost.
    """
    value = -cost
    for cue_l in (False, True):
        py = cue_probability(p, q, cue_l)
        post = posterior_p_left(p, q, cue_l)
        v_l, v_r = commit_values(post, r_win, r_lose)
        value += py * max(v_l, v_r)
    return value


def mutual_information_state_cue(p: float, q: float) -> float:
    """
    I(Z;Y) for a binary symmetric cue channel with reliability q.
    Natural-log units (nats).
    """
    p_y_l = cue_probability(p, q, True)
    return binary_entropy(p_y_l) - binary_entropy(q)


def softmax(values: np.ndarray, beta: float) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    z = beta * (values - values.max())
    exp_z = np.exp(z)
    return exp_z / exp_z.sum()


@dataclass(frozen=True)
class Condition:
    p_left: float
    cue_reliability: float
    sample_cost: float
    safe_reward: float = 0.55
    r_win: float = 1.0
    r_lose: float = 0.0


def action_scores(cond: Condition, alpha_epi: float = 1.0) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Returns:
        scores_aif, scores_brl, information_gain

    BRL = Bayes-optimal instrumental value.
    AIF = same instrumental value + epistemic value for SAMPLE.

    With log outcome preferences proportional to reward, maximizing the AIF score
    corresponds to minimizing a reduced expected free energy:
        G = - E[log P_pref(o)] - I(Z;Y)
    up to additive/scaling constants.
    """
    p = cond.p_left
    q = cond.cue_reliability
    c = cond.sample_cost

    v_l, v_r = commit_values(p, cond.r_win, cond.r_lose)
    v_sample = sample_instrumental_value(p, q, c, cond.r_win, cond.r_lose)
    ig = mutual_information_state_cue(p, q)

    brl = np.array([cond.safe_reward, v_l, v_r, v_sample], dtype=float)
    aif = brl.copy()
    aif[3] += alpha_epi * ig
    return aif, brl, ig


def action_probabilities(
    cond: Condition, beta: float = 8.0, alpha_epi: float = 1.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    aif_scores, brl_scores, ig = action_scores(cond, alpha_epi)
    p_aif = softmax(aif_scores, beta)
    p_brl = softmax(brl_scores, beta)
    return p_aif, p_brl, aif_scores, brl_scores, ig


def kl(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    mask = p > 0
    return float(np.sum(p[mask] * np.log(p[mask] / q[mask])))


def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    m = 0.5 * (p + q)
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def grid_search(
    p_grid=None,
    q_grid=None,
    cost_grid=None,
    beta: float = 8.0,
    alpha_epi: float = 1.0,
    safe_reward: float = 0.55,
) -> List[Dict[str, float]]:
    if p_grid is None:
        p_grid = np.linspace(0.50, 0.95, 46)
    if q_grid is None:
        q_grid = np.linspace(0.55, 0.95, 41)
    if cost_grid is None:
        cost_grid = np.linspace(0.00, 0.40, 41)

    rows = []
    for p in p_grid:
        for q in q_grid:
            for c in cost_grid:
                cond = Condition(float(p), float(q), float(c), safe_reward=safe_reward)
                pa, pb, sa, sb, ig = action_probabilities(cond, beta, alpha_epi)
                rows.append(
                    {
                        "js_divergence": js_divergence(pa, pb),
                        "prior_p_left": p,
                        "cue_reliability": q,
                        "sample_cost": c,
                        "information_gain_nats": ig,
                        "P_AIF_SAFE": pa[0],
                        "P_AIF_COMMIT_L": pa[1],
                        "P_AIF_COMMIT_R": pa[2],
                        "P_AIF_SAMPLE": pa[3],
                        "P_BRL_SAFE": pb[0],
                        "P_BRL_COMMIT_L": pb[1],
                        "P_BRL_COMMIT_R": pb[2],
                        "P_BRL_SAMPLE": pb[3],
                        "AIF_SAMPLE_SCORE": sa[3],
                        "BRL_SAMPLE_SCORE": sb[3],
                    }
                )
    rows.sort(key=lambda r: r["js_divergence"], reverse=True)
    return rows


def simulate_choices(probs: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    return rng.choice(len(ACTIONS), size=n, p=probs)


def log_predictive_density(choices: np.ndarray, probs: np.ndarray) -> float:
    return float(np.sum(np.log(np.maximum(probs[choices], 1e-15))))


def recovery_demo(
    cond: Condition, n_trials: int = 200, beta: float = 8.0, alpha_epi: float = 1.0, seed: int = 1
) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    pa, pb, _, _, _ = action_probabilities(cond, beta, alpha_epi)

    choices_from_aif = simulate_choices(pa, n_trials, rng)
    choices_from_brl = simulate_choices(pb, n_trials, rng)

    return {
        "AIF_data_LPD_AIF": log_predictive_density(choices_from_aif, pa),
        "AIF_data_LPD_BRL": log_predictive_density(choices_from_aif, pb),
        "AIF_data_delta": log_predictive_density(choices_from_aif, pa)
        - log_predictive_density(choices_from_aif, pb),
        "BRL_data_LPD_AIF": log_predictive_density(choices_from_brl, pa),
        "BRL_data_LPD_BRL": log_predictive_density(choices_from_brl, pb),
        "BRL_data_delta": log_predictive_density(choices_from_brl, pa)
        - log_predictive_density(choices_from_brl, pb),
    }


def write_csv(path: str, rows: List[Dict[str, float]], top_n: int = 100):
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in rows[:top_n]:
            w.writerow(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--beta", type=float, default=8.0)
    ap.add_argument("--alpha-epi", type=float, default=1.0)
    ap.add_argument("--safe-reward", type=float, default=0.55)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--csv", type=str, default="reduced_aif_v1_top_conditions.csv")
    args = ap.parse_args()

    rows = grid_search(beta=args.beta, alpha_epi=args.alpha_epi, safe_reward=args.safe_reward)
    write_csv(args.csv, rows, top_n=max(args.top, 100))

    print("Top discriminating conditions")
    print("=" * 80)
    for i, r in enumerate(rows[: args.top], 1):
        print(
            f"{i:2d}. JS={r['js_divergence']:.4f} | "
            f"pL={r['prior_p_left']:.2f} q={r['cue_reliability']:.2f} "
            f"cost={r['sample_cost']:.2f} | "
            f"Psample(AIF)={r['P_AIF_SAMPLE']:.3f} "
            f"Psample(BRL)={r['P_BRL_SAMPLE']:.3f}"
        )

    best = rows[0]
    cond = Condition(
        best["prior_p_left"],
        best["cue_reliability"],
        best["sample_cost"],
        safe_reward=args.safe_reward,
    )
    print("\nRecovery demo at best condition")
    print("=" * 80)
    for k, v in recovery_demo(cond, n_trials=200, beta=args.beta, alpha_epi=args.alpha_epi).items():
        print(f"{k}: {v:.3f}")


if __name__ == "__main__":
    main()
