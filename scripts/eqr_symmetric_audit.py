#!/usr/bin/env python3
"""EQR falsification on the shipped symmetric-cue probe algebra.

Compiles named controllers to behavior under a frozen probe set, then
reports:
  - exact quotient (max |Delta P| <= 1e-8): a true equivalence relation
  - single-linkage clusters at practical tolerances (NOT transitive)

Does not implement asymmetric v6 channels. Those predictions stay
UNVERIFIED until that probe algebra exists in code.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "artifacts"))

from reduced_aif_v1 import (  # noqa: E402
    Condition,
    action_scores,
    binary_entropy,
    softmax,
)

OUT = ROOT / "artifacts" / "eqr_symmetric_audit.json"


def probes() -> list[Condition]:
    grid = []
    for p in (0.50, 0.64, 0.80):
        for q in (0.60, 0.80, 0.95):
            for c in (0.00, 0.20, 0.40):
                grid.append(Condition(p, q, c))
    return grid


def policy(cond: Condition, sample_bonus: float, beta: float) -> np.ndarray:
    _aif, brl, _ig = action_scores(cond, alpha_epi=0.0)
    scores = brl.copy()
    scores[3] += sample_bonus
    return softmax(scores, beta)


def curiosity_bonus(cond: Condition, kappa: float, gamma: float) -> float:
    # Preprint eq. (5): kappa * H(Z) * (2q - 1)^gamma, nats.
    return kappa * binary_entropy(cond.p_left) * (2.0 * cond.cue_reliability - 1.0) ** gamma


def controllers() -> list[tuple[str, str]]:
    """(name, family). Behavior is filled by compile()."""
    rows = [
        ("instr_b8", "instrumental"),
        ("exact_mi_a0.25_b8", "exact_mi"),
        ("exact_mi_a0.5_b8", "exact_mi"),
        ("exact_mi_a1_b8", "exact_mi"),
        ("exact_mi_a1_b8_copy", "exact_mi_rename"),
        ("exact_mi_a2_b8", "exact_mi"),
        ("exact_mi_a4_b8", "exact_mi"),
        ("exact_mi_a1_b2", "exact_mi_beta"),
        ("exact_mi_a1_b4", "exact_mi_beta"),
        ("exact_mi_a1_b16", "exact_mi_beta"),
    ]
    for kappa in (0.5, 1.0, 2.0):
        for gamma in (1.0, 2.0, 4.0):
            rows.append((f"cur_k{kappa:g}_g{gamma:g}_b8", "curiosity"))
    return rows


def bonus_and_beta(name: str, cond: Condition) -> tuple[float, float]:
    if name.startswith("instr"):
        return 0.0, 8.0
    if name.startswith("exact_mi_a"):
        # exact_mi_a{alpha}_b{beta}[_copy]
        body = name.removeprefix("exact_mi_a").removesuffix("_copy")
        alpha_s, beta_s = body.split("_b")
        alpha = float(alpha_s)
        _aif, _brl, ig = action_scores(cond, alpha_epi=alpha)
        return alpha * ig, float(beta_s)
    if name.startswith("cur_"):
        # cur_k{kappa}_g{gamma}_b8
        body = name.removeprefix("cur_k")
        kappa_s, rest = body.split("_g")
        gamma_s, beta_s = rest.split("_b")
        return curiosity_bonus(cond, float(kappa_s), float(gamma_s)), float(beta_s)
    raise KeyError(name)


def policy_vector(name: str, probe_list: list[Condition]) -> np.ndarray:
    chunks = []
    for cond in probe_list:
        bonus, beta = bonus_and_beta(name, cond)
        chunks.append(policy(cond, bonus, beta))
    return np.concatenate(chunks)


def compile_matrix(names: list[str], probe_list: list[Condition]) -> np.ndarray:
    cols = []
    for name in names:
        vec = []
        for cond in probe_list:
            bonus, beta = bonus_and_beta(name, cond)
            vec.append(policy(cond, bonus, beta))
        cols.append(np.concatenate(vec))
    return np.vstack(cols)


def connected_components(dist: np.ndarray, eps: float) -> list[list[int]]:
    n = dist.shape[0]
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i in range(n):
        for j in range(i + 1, n):
            if dist[i, j] <= eps:
                union(i, j)
    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def max_abs_distance(matrix: np.ndarray) -> np.ndarray:
    n = matrix.shape[0]
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.max(np.abs(matrix[i] - matrix[j])))
            dist[i, j] = dist[j, i] = d
    return dist


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    probe_list = probes()
    named = controllers()
    names = [n for n, _ in named]
    families = {n: f for n, f in named}
    matrix = compile_matrix(names, probe_list)
    dist = max_abs_distance(matrix)

    exact = connected_components(dist, 1e-8)
    practical = {str(eps): connected_components(dist, eps) for eps in (0.02, 0.05)}

    def pack(groups: list[list[int]]) -> list[dict]:
        out = []
        for g in sorted(groups, key=lambda xs: (-len(xs), xs[0])):
            members = [names[i] for i in g]
            out.append(
                {
                    "size": len(members),
                    "members": members,
                    "families": sorted({families[m] for m in members}),
                }
            )
        return out

    n_h = len(names)
    n_exact = len(exact)
    report = {
        "probe_algebra": "symmetric cue only: P(Y=Z)=q; actions SAFE/COMMIT_L/COMMIT_R/SAMPLE",
        "n_probes": len(probe_list),
        "observable": "full 4-action softmax policy on every probe",
        "distance": "max absolute probability difference over probes and actions",
        "n_raw_hypotheses": n_h,
        "n_exact_classes_eps_1e-8": n_exact,
        "quotient_compression_exact": n_h / n_exact,
        "exact_classes": pack(exact),
        "single_linkage_not_equivalence": practical_summary(practical, names, families, n_h),
        "note": (
            "Tolerance clustering is single-linkage and is not a mathematical "
            "equivalence relation. Exact classes use eps=1e-8. Asymmetric v6 "
            "probes are outside this audit."
        ),
    }
    # nearest cross-family pair
    best = None
    for i, ni in enumerate(names):
        for j in range(i + 1, n_h):
            nj = names[j]
            if families[ni] == families[nj]:
                continue
            if families[ni].startswith("exact_mi") and families[nj].startswith("exact_mi"):
                continue
            d = float(dist[i, j])
            if best is None or d < best[0]:
                best = (d, ni, nj, families[ni], families[nj])
    if best:
        report["closest_cross_family"] = {
            "max_abs_delta_p": best[0],
            "a": best[1],
            "b": best[2],
            "family_a": best[3],
            "family_b": best[4],
        }

    target = policy_vector("exact_mi_a1_b8", probe_list)
    best_cur = None
    for kappa in np.linspace(0.0, 4.0, 17):
        for gamma in np.linspace(0.5, 6.0, 12):
            vec = []
            for cond in probe_list:
                bonus = curiosity_bonus(cond, float(kappa), float(gamma))
                vec.append(policy(cond, bonus, 8.0))
            d = float(np.max(np.abs(np.concatenate(vec) - target)))
            if best_cur is None or d < best_cur[0]:
                best_cur = (d, float(kappa), float(gamma))
    profile = []
    for cond in probe_list:
        target_p = policy(cond, action_scores(cond, alpha_epi=1.0)[2], 8.0)
        # action_scores(..., 1)[2] is I(Z;Y); exact-MI bonus at alpha=1 is that IG.
        best_d = None
        best_kg = None
        for kappa in np.linspace(0.0, 4.0, 17):
            for gamma in np.linspace(0.5, 6.0, 12):
                bonus = curiosity_bonus(cond, float(kappa), float(gamma))
                d = float(np.max(np.abs(policy(cond, bonus, 8.0) - target_p)))
                if best_d is None or d < best_d:
                    best_d = d
                    best_kg = (float(kappa), float(gamma))
        profile.append(
            {
                "p": cond.p_left,
                "q": cond.cue_reliability,
                "c": cond.sample_cost,
                "min_max_abs_delta_p": best_d,
                "kappa": best_kg[0],
                "gamma": best_kg[1],
            }
        )
    worst = max(profile, key=lambda r: r["min_max_abs_delta_p"])
    report["curiosity_family_profile_vs_exact_mi"] = {
        "definition": (
            "For each probe separately, minimize max|dP| over (kappa, gamma). "
            "This is class-level overlap, not one hypothesis."
        ),
        "worst_probe": worst,
        "n_probes_below_0.02": sum(1 for r in profile if r["min_max_abs_delta_p"] <= 0.02),
        "n_probes": len(profile),
    }

    report["best_fixed_curiosity_vs_exact_mi_a1_b8"] = {
        "max_abs_delta_p": best_cur[0],
        "kappa": best_cur[1],
        "gamma": best_cur[2],
        "beta": 8.0,
        "interpretation": (
            "One (kappa, gamma) pair scored on every probe. "
            "This is not the preprint v4 grid search and does not certify v4."
        ),
    }

    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"raw hypotheses: {n_h}")
    print(f"exact classes (eps=1e-8): {n_exact}")
    print(f"QC exact: {n_h / n_exact:.3f}")
    print("exact classes with size>1:")
    for c in report["exact_classes"]:
        if c["size"] > 1:
            print(f"  {c['members']}")
    for eps, summary in report["single_linkage_not_equivalence"].items():
        print(f"single-linkage eps={eps}: classes={summary['n_classes']} QC={summary['qc']:.3f}")
    if best:
        print(f"closest cross-family: {best[1]} vs {best[2]} max|dP|={best[0]:.4f}")
    bc = report["best_fixed_curiosity_vs_exact_mi_a1_b8"]
    print(
        f"best fixed curiosity vs exact-MI a=1 b=8: "
        f"max|dP|={bc['max_abs_delta_p']:.4f} kappa={bc['kappa']} gamma={bc['gamma']}"
    )
    prof = report["curiosity_family_profile_vs_exact_mi"]
    w = prof["worst_probe"]
    print(
        f"curiosity family profile: {prof['n_probes_below_0.02']}/{prof['n_probes']} "
        f"probes within 0.02; worst max|dP|={w['min_max_abs_delta_p']:.4f} "
        f"at p={w['p']} q={w['q']} c={w['c']}"
    )
    print("wrote", OUT)


def practical_summary(groups_by_eps, names, families, n_h):
    out = {}
    for eps, groups in groups_by_eps.items():
        packed = []
        for g in sorted(groups, key=lambda xs: (-len(xs), xs[0])):
            members = [names[i] for i in g]
            packed.append(
                {
                    "size": len(members),
                    "members": members,
                    "families": sorted({families[m] for m in members}),
                }
            )
        n_c = len(groups)
        out[eps] = {"n_classes": n_c, "qc": n_h / n_c, "classes": packed}
    return out


if __name__ == "__main__":
    main()
