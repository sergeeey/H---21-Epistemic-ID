"""Asymmetric binary cue channel for the matched-pair probe algebra.

a = P(Y=L | Z=L), b = P(Y=R | Z=R).
Mean accuracy q_bar = P(Y=Z) = p*a + (1-p)*b.
This is the probe extension that symmetric q cannot express.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from reduced_aif_v1 import binary_entropy, commit_values, softmax


@dataclass(frozen=True)
class Channel:
    p_left: float
    sensitivity: float  # a
    specificity: float  # b
    sample_cost: float = 0.0
    safe_reward: float = 0.55
    r_win: float = 1.0
    r_lose: float = 0.0

    def mean_accuracy(self) -> float:
        p, a, b = self.p_left, self.sensitivity, self.specificity
        return p * a + (1.0 - p) * b

    def p_y_left(self) -> float:
        p, a, b = self.p_left, self.sensitivity, self.specificity
        return p * a + (1.0 - p) * (1.0 - b)

    def ambiguity_nats(self) -> float:
        """H(Y|Z) = p H(a) + (1-p) H(b). Not held fixed by mean-accuracy matching."""
        p = self.p_left
        return p * binary_entropy(self.sensitivity) + (1.0 - p) * binary_entropy(self.specificity)

    def mutual_information_nats(self) -> float:
        py = self.p_y_left()
        if py <= 0.0 or py >= 1.0:
            h_y = 0.0
        else:
            h_y = binary_entropy(py)
        return h_y - self.ambiguity_nats()

    def posterior_left(self, y_left: bool) -> float:
        p, a, b = self.p_left, self.sensitivity, self.specificity
        if y_left:
            num = p * a
            den = self.p_y_left()
        else:
            num = p * (1.0 - a)
            den = 1.0 - self.p_y_left()
        if den <= 0.0:
            return p
        return num / den

    def gross_classification_value(self) -> float:
        """E[max commit value | Y], before sampling cost."""
        total = 0.0
        py_l = self.p_y_left()
        for y_left, py in ((True, py_l), (False, 1.0 - py_l)):
            if py <= 0.0:
                continue
            post = self.posterior_left(y_left)
            v_l, v_r = commit_values(post, self.r_win, self.r_lose)
            total += py * max(v_l, v_r)
        return total

    def instrumental_sample_value(self) -> float:
        return self.gross_classification_value() - self.sample_cost

    def action_scores(self, sample_bonus: float) -> np.ndarray:
        p = self.p_left
        v_l, v_r = commit_values(p, self.r_win, self.r_lose)
        return np.array(
            [self.safe_reward, v_l, v_r, self.instrumental_sample_value() + sample_bonus],
            dtype=float,
        )

    def policy(self, sample_bonus: float, beta: float = 8.0) -> np.ndarray:
        return softmax(self.action_scores(sample_bonus), beta)


def specificity_for_mean_accuracy(p: float, a: float, q_bar: float) -> float:
    if abs(1.0 - p) < 1e-15:
        raise ValueError("p=1 leaves b unidentified")
    return (q_bar - p * a) / (1.0 - p)


def curiosity_bonus(p: float, q_bar: float, kappa: float, gamma: float) -> float:
    """Coarse bonus uses only prior entropy and mean accuracy, not (a, b)."""
    return kappa * binary_entropy(p) * (2.0 * q_bar - 1.0) ** gamma


def cost_match(channel: Channel, target_instrumental: float) -> Channel:
    """Choose c so instrumental sample value equals the target."""
    c = channel.gross_classification_value() - target_instrumental
    return Channel(
        channel.p_left,
        channel.sensitivity,
        channel.specificity,
        sample_cost=c,
        safe_reward=channel.safe_reward,
        r_win=channel.r_win,
        r_lose=channel.r_lose,
    )


def valid_channel(p: float, a: float, q_bar: float) -> Channel | None:
    try:
        b = specificity_for_mean_accuracy(p, a, q_bar)
    except ValueError:
        return None
    if not (0.01 < a < 0.99 and 0.01 < b < 0.99):
        return None
    if min(a, b) <= 0.5:
        return None
    ch = Channel(p, a, b)
    if ch.p_y_left() <= 1e-9 or ch.p_y_left() >= 1.0 - 1e-9:
        return None
    if not math.isfinite(ch.mutual_information_nats()):
        return None
    return ch
