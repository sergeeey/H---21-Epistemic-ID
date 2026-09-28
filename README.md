# Structural Identifiability of Epistemic Value in Active Inference

**A matched-channel experimental design**

Research note · Version 1.1 · 28 September 2026

**Status:** METHOD PROPOSED · SYNTHETICALLY IDENTIFIABLE · HUMAN VALIDATION PENDING

Internal project identifier: `AIF-KILL-001` (not a public title).

Public repository: https://github.com/sergeeey/H---21-Epistemic-ID

This repository ships the **v1 reduced simulation** used to check mutual-information units and to separate an EFE-derived exact-MI controller from a reward-only Bayesian controller. The later adversarial sequence (generic curiosity, structural pair search, matched asymmetric channels, equivalence ceiling) is reported in the preprint. The full v4–v8 search pipeline is **not** in this repository.

A close human prior-art precedent is Nelson et al. (2010), Experiment 3, Condition 1: same prior, same probability gain, different information gain. Independent recalculation: `python scripts/recompute_nelson_condition1.py`. Design-class novelty of v6 is **not supported**. See [docs/nelson_2010_v6_mapping.md](docs/nelson_2010_v6_mapping.md).

The FEP-audit file in [docs/sources/](docs/sources/) is a **positioning** source (Motivation / Scope / programme map). It is not evidence for v6. See [docs/research_programme.md](docs/research_programme.md) and [docs/estimand.md](docs/estimand.md).

## One-command reproduction

```bash
python scripts/reproduce.py
```

Requires Python 3.10+ and `numpy`.

The command checks three things:

1. `I(Z;Y) ≈ 0.4625` nats for `p = 0.64`, `q = 0.95` (a value near `0.953` is bits, not nats).
2. Action scores and sampling probabilities at the published top v1 condition.
3. A compact discrimination grid in which the reduced exact-MI controller samples more than reward-only control.
4. Nelson 2010 Condition 1: probability gain and accuracy tied; I(F) > I(G).

None of these rates may be used to choose participant sample size.

## Documents

| File | Role |
|---|---|
| [outreach/Structural_Identifiability_Matched_Channel_Research_Brief_v1.1.pdf](outreach/Structural_Identifiability_Matched_Channel_Research_Brief_v1.1.pdf) | 2-page brief |
| [Structural_Identifiability_Epistemic_Value_Active_Inference_v1.1.pdf](Structural_Identifiability_Epistemic_Value_Active_Inference_v1.1.pdf) | Preprint v1.1 |
| [outreach/letters/](outreach/letters/) | Draft Wave-1 emails (not sent) |

## What the reduced model is

One-step hidden-context task. Hidden state `Z ∈ {L,R}`. Actions: SAFE, COMMIT_L, COMMIT_R, SAMPLE. After sampling a cue, the agent commits optimally.

- Instrumental controller: expected reward only.
- Reduced AIF controller: same instrumental values plus `α_epi * I(Z;Y)` on SAMPLE, derived from expected free energy when log-preferences are proportional to reward.

This tests an **EFE-derived epistemic-value component**. It does not test the entirety of Active Inference.

## Non-claims

- No human data have been collected.
- No “first” or “breakthrough” novelty claim.
- v8 is a preregistration-**oriented** candidate protocol, not preregistration-ready.
- A same-objective alternative with the same policy mapping is behaviorally indistinguishable (v7).
- v6 discriminates the tested accuracy-based curiosity family; it does not discriminate all information-seeking algorithms.

## License

MIT. See [LICENSE](LICENSE).
