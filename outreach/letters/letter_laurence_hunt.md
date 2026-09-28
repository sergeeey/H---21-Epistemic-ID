# Wave 1 draft — Laurence Hunt (Oxford, Laboratory of Decision Dynamics)

Status: DRAFT. Do not send until the brief PDF, preprint PDF, and `python scripts/reproduce.py` are publicly reachable.

Suggested subject:

`Matched-channel task for distinguishing exact information gain from generic search`

---

Dear Professor Hunt,

Your group’s work on decision making as it unfolds with information search — including the formalization of planning and search in naturalistic settings — is the closest empirical neighbour I have found to a design problem I cannot finish from simulation alone.

The problem is identifiability, not a new utility. In a one-step cue-sampling task, a flexible curiosity bonus that uses only uncertainty and mean cue accuracy can become nearly observationally equivalent to a controller that scores sampling by exact mutual information. We built matched asymmetric channels: same prior, same mean accuracy, same instrumental value of sampling, different exact I(Z;Y). Synthetically, the exact-MI controller predicts a large within-pair sampling contrast and the coarse curiosity family predicts essentially none.

Nelson et al. (2010) already ran a close human OED contrast — same prior, same probability gain, different information gain — and only 12/22 participants preferred the higher-IG feature after experience-based learning. I am therefore not proposing a first matched-channel experiment. I am asking whether an Active Inference / sequential-decision framing changes that older result, and whether asymmetric contingencies remain learnable when sampling is an explicit costly action rather than a feature choice.

The remaining bottleneck is human feasibility. Participants may fail to learn asymmetric contingencies; heterogeneity may wash out the contrast; simple heuristics may reproduce it. Those are experimental questions about information search, not Active Inference advocacy. A later positive result would support sensitivity to exact channel information geometry relative to specified alternatives. It would not identify a unique theoretical derivation: any other theory that implements the same objective and policy mapping is behaviorally equivalent.

I have a 2-page brief, a v1.1 methods preprint, and a one-command reproduction of the shipped synthetic checks. I am looking for a collaborator who already runs human information-search experiments to help judge whether this geometry is learnable, and to co-design a small feasibility pilot if it is. I would contribute the design, models, and analysis pipeline; your group would contribute task expertise, recruitment / ethics infrastructure, and interpretation.

Would a short conversation be useful?

Sincerely,  
[Your name]  
[Your affiliation]  
[Email]  
Brief: https://github.com/sergeeey/H---21-Epistemic-ID/blob/main/outreach/Structural_Identifiability_Matched_Channel_Research_Brief_v1.1.pdf  
Preprint: https://github.com/sergeeey/H---21-Epistemic-ID/blob/main/Structural_Identifiability_Epistemic_Value_Active_Inference_v1.1.pdf  
Code: https://github.com/sergeeey/H---21-Epistemic-ID — `python scripts/reproduce.py`

---

Pitch used: computationally optimized information-search task; the bottleneck is human learnability of asymmetric contingencies.  
Do not lead with FEP. Hunt/Daw already share a literature on planning and search; keep the ask empirical.
