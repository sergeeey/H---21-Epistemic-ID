# Formal mapping: Nelson et al. 2010 Condition 1 ↔ v6

Status: EXP-001 complete as a structural comparison, not as identity.  
Date: 28 September 2026  
Source paper: Nelson JD, McKenzie CRM, Cottrell GW, Sejnowski TJ. Experience matters: Information acquisition optimizes probability gain. *Psychological Science*. 2010;21(7):960–969. doi:10.1177/0956797610372637

## Verdict

Nelson et al. 2010, Experiment 3, Condition 1 is a **structural analogue** of v6, not a completed run of v6.

They independently implemented:

same prior + same instrumental classification value + different exact information gain.

They already collected human data. Therefore:

- “v6 is a historically new structural discriminator” is **not supported**.
- “Nelson already ran our v6 experiment” is **also not supported**.

The remaining scientific question is what, if anything, an Active Inference decision framing adds beyond this older Optimal Experimental Design (OED) contrast.

## Independent recalculation [VERIFIED]

Condition: \(P(a)=0.50\), \(P(f_1|a)=0\), \(P(f_1|b)=0.50\), \(P(g_1|a)=0.25\), \(P(g_1|b)=0.75\).

| Channel | Prior | Bayes-optimal accuracy | Probability gain | Mutual information |
|---|---:|---:|---:|---:|
| F | 0.50 | 0.75 | 0.25 | 0.2158 nats |
| G | 0.50 | 0.75 | 0.25 | 0.1308 nats |

Reproduce:

```bash
python scripts/recompute_nelson_condition1.py
```

The paper’s stated PG = 0.25 for both features is recovered exactly. Feature F has higher MI, as claimed. Human result reported by the authors: 12/22 (55%) preferred F after experience-based learning. A descriptive Wilson interval around 12/22 is approximately [0.35, 0.73]. That is **not** a strong preference for the higher-IG channel, and it is **not** a precise original-paper null test.

## Where the utilities line up

For 0–1 classification reward, Nelson’s probability gain is the expected increase in the probability of a correct category guess:

\[
\mathrm{PG}(F)=\mathbb{E}[\max_c P(c\mid F)]-\max_c P(c).
\]

In the v6 one-step task with \(r_{\mathrm{win}}=1\), \(r_{\mathrm{lose}}=0\), the expected instrumental value of a free cue is the same expected posterior-optimal classification accuracy, minus any sampling cost. Therefore, **when sampling cost is zero and the only payoff is correct classification**,

\[
\mathrm{PG}\ \text{tied}\ \iff\ \text{instrumental value of information tied}.
\]

That is the legitimate bridge. It is an assumption, not a theorem about the two full tasks.

## Where the tasks diverge

| Element | Nelson 2010, E3 C1 | v6 matched-channel design |
|---|---|---|
| Choice | Which feature to view (F vs G) | Whether to SAMPLE a given channel vs SAFE / COMMIT |
| Cost | No explicit sampling cost | Cost-matched so instrumental SAMPLE value is equal across a pair |
| Held constant | Prior, probability gain | Prior, mean cue accuracy \(\bar q\), instrumental SAMPLE value |
| Varied | Information gain (and certainty possibility on F) | Exact \(I(Z;Y)\) |
| Channel zeros | F has \(P(f_1|a)=0\) (certainty possible) | Typical v6 pairs do not use zero-likelihood cells |
| Prior | 0.50 | Candidate pairs use 0.70 and 0.80 |
| Rival set | IG, KL, impact, probability-of-certainty | Instrumental Bayes + coarse curiosity; IDS/UCB/Thompson not implemented |
| Human N | 22 in this cell | None yet |
| Process / AIF | OED utilities only | Reduced EFE score + v7 same-objective ceiling |

Nelson also found that **experience-based vs statistics-based presentation** changes search (their Experiments 1–2). That is directly relevant to R1 (learnability of asymmetric contingencies) and H3 (representation dependence).

## Kill criteria for novelty

If someone asks “is the matched same-accuracy / different-MI idea new?”:

- **Closed as a design-class novelty claim.** Nelson 2005 already searched for environments where OED utilities diverge; Nelson et al. 2010 built and tested one.

If someone asks “is the v6 *task* new?”:

- **Open.** Four-action SAMPLE/COMMIT structure, cost matching, curiosity-family rival, and AIF/EFE reduced mapping are not in Nelson 2010.

If someone asks “will humans show a large exact-MI sampling contrast in v6?”:

- **Weakened prior, not killed.** A close human cell was near chance. The tasks are not identical, and 12/22 is a small sample.

## What this does to the project

Do **not** launch a new human pilot as the next action.

Do, in order:

1. Keep this mapping and the independent recalculation in the public package. **Done here.**
2. Attempt to obtain Nelson trial-level data or supplementary materials (EXP-002). Not done.
3. Only then design a pilot as an AIF-framed *replication/extension* of the OED contrast, not as a first demonstration of matched channels.

## Claim updates

| ID | Claim | Status |
|---|---|---|
| C-001 | Generic information seeking uniquely supports AIF | Contradicted |
| C-002 | v6 matched-channel construction is historically new as a design class | Substantially weakened |
| C-003 | No relevant human test exists | Contradicted |
| C-004 | Exact-MI behavior would prove AIF | Contradicted (already by v7) |
| C-005 | Project remains valuable as an AIF-specific extension of older OED work | Plausible |
