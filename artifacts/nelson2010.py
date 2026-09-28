"""Independent recalculation of Nelson et al. (2010), Experiment 3, Condition 1.

Source: Nelson JD, McKenzie CRM, Cottrell GW, Sejnowski TJ.
Experience matters: Information acquisition optimizes probability gain.
Psychological Science. 2010;21(7):960-969. doi:10.1177/0956797610372637

Condition 1 (experience-based):
    P(a) = 0.50
    P(f1|a) = 0,   P(f1|b) = 0.50
    P(g1|a) = 0.25, P(g1|b) = 0.75

The paper states both features have probability gain 0.25, while F has
higher information gain. Human result: 12/22 (55%) preferred F.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log(p) + (1.0 - p) * math.log(1.0 - p))


@dataclass(frozen=True)
class FeatureChannel:
    name: str
    prior_a: float
    p_pos_given_a: float
    p_pos_given_b: float

    @property
    def prior_b(self) -> float:
        return 1.0 - self.prior_a

    @property
    def p_pos(self) -> float:
        return self.p_pos_given_a * self.prior_a + self.p_pos_given_b * self.prior_b

    def posterior_a(self, observed_pos: bool) -> float:
        if observed_pos:
            num = self.p_pos_given_a * self.prior_a
            den = self.p_pos
        else:
            num = (1.0 - self.p_pos_given_a) * self.prior_a
            den = 1.0 - self.p_pos
        return num / den

    def expected_accuracy(self) -> float:
        acc = 0.0
        for pos, py in ((True, self.p_pos), (False, 1.0 - self.p_pos)):
            pa = self.posterior_a(pos)
            acc += py * max(pa, 1.0 - pa)
        return acc

    def prior_accuracy(self) -> float:
        return max(self.prior_a, self.prior_b)

    def probability_gain(self) -> float:
        return self.expected_accuracy() - self.prior_accuracy()

    def mutual_information_nats(self) -> float:
        # I(C; Feature) = H(Feature) - H(Feature | C)
        h_feat = binary_entropy(self.p_pos)
        h_cond = self.prior_a * binary_entropy(self.p_pos_given_a) + self.prior_b * binary_entropy(
            self.p_pos_given_b
        )
        return h_feat - h_cond


F = FeatureChannel("F", 0.50, 0.00, 0.50)
G = FeatureChannel("G", 0.50, 0.25, 0.75)


def condition1_table() -> list[dict[str, float | str]]:
    rows = []
    for ch in (F, G):
        rows.append(
            {
                "channel": ch.name,
                "prior": ch.prior_a,
                "bayes_optimal_accuracy": ch.expected_accuracy(),
                "probability_gain": ch.probability_gain(),
                "mutual_information_nats": ch.mutual_information_nats(),
            }
        )
    return rows


def assert_paper_claims() -> None:
    assert abs(F.probability_gain() - 0.25) < 1e-12
    assert abs(G.probability_gain() - 0.25) < 1e-12
    assert abs(F.expected_accuracy() - 0.75) < 1e-12
    assert abs(G.expected_accuracy() - 0.75) < 1e-12
    assert abs(F.mutual_information_nats() - 0.21576155433883565) < 1e-9
    assert abs(G.mutual_information_nats() - 0.13081203594113694) < 1e-9
    assert F.mutual_information_nats() > G.mutual_information_nats()
