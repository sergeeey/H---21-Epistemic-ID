# Wave 1 draft — Laurence Hunt (Oxford, Laboratory of Decision Dynamics)

Status: DRAFT pending delta re-audit. Do not send until the send-gate checklist is green.

Suggested subject:

`Information search after Nelson 2010: what an AIF-framed extension would need to justify`

---

Dear Professor Hunt,

Your group’s work on decision making as it unfolds with information search — for example the line of work on temporally extended and naturalistic choice paradigms at the Laboratory of Decision Dynamics — is the closest empirical neighbour I have found to a design problem I cannot finish from simulation alone.

The problem is identifiability, not a new utility. In a one-step cue-sampling task, a flexible curiosity bonus that uses only uncertainty and mean cue accuracy can become nearly observationally equivalent to a controller that scores sampling by exact mutual information. In the preprint I report matched asymmetric channels (same prior, same mean accuracy, same instrumental value of sampling, different exact I(Z;Y)) under which the exact-MI controller predicts a large within-pair sampling contrast and the coarse curiosity family predicts essentially none. The public repository currently reproduces the shipped v1 and Nelson checks; the broader v4–v8 adversarial sequence is documented in the preprint but is not yet packaged for end-to-end public reproduction.

Nelson et al. (2010) already ran a close human OED contrast — same prior, same probability gain, different information gain — and only 12/22 participants preferred the higher-IG feature after experience-based learning. I am therefore not proposing a first matched-channel experiment, and I am not asking first for a recruitment slot. The ordered next gate is EXP-002: obtain or reconstruct Nelson trial-level / supplementary materials and reanalyse whether an AIF / sequential-decision framing changes that older result when sampling is an explicit costly action rather than a feature choice. The probability-gain rival that won in Nelson's data is not yet implemented in my comparison set — that is, in my view, the first thing the design still owes. A later feasibility pilot would ask whether asymmetric contingencies remain learnable; that step comes only if EXP-002 keeps the question informative.

A later positive result would support sensitivity to exact channel information geometry relative to specified alternatives. It would not identify a unique theoretical derivation: any other theory that implements the same objective and policy mapping is behaviorally equivalent.

I have a 2-page brief, a v1.1 methods preprint, and a one-command reproduction of the shipped synthetic checks. Critical comments on the Nelson mapping, or pointers to raw / supplementary materials, would already be useful; co-design of a post-EXP-002 feasibility gate would come later if warranted.

Would a short conversation be useful?

Sincerely,  
Sergey Boyko  
Independent researcher  
sergeikuch80@gmail.com  
Brief: https://github.com/sergeeey/H---21-Epistemic-ID/blob/main/outreach/Structural_Identifiability_Matched_Channel_Research_Brief_v1.1.pdf  
Preprint: https://github.com/sergeeey/H---21-Epistemic-ID/blob/main/Structural_Identifiability_Epistemic_Value_Active_Inference_v1.1.pdf  
Code: https://github.com/sergeeey/H---21-Epistemic-ID — `python scripts/reproduce.py`

---

Pitch used: information-search feasibility after cheaper Nelson reanalysis; do not lead with FEP.
