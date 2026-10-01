import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "artifacts"))

from asymmetric_channel import (  # noqa: E402
    Channel,
    cost_match,
    curiosity_bonus,
    valid_channel,
)
from reduced_aif_v1 import (  # noqa: E402
    mutual_information_state_cue,
    sample_instrumental_value,
)


def test_symmetric_channel_matches_shipped_mi_and_instrumental():
    p, q, c = 0.64, 0.95, 0.40
    ch = Channel(p, q, q, sample_cost=c)
    assert ch.mutual_information_nats() == pytest.approx(mutual_information_state_cue(p, q))
    assert ch.instrumental_sample_value() == pytest.approx(sample_instrumental_value(p, q, c))


def test_matched_pair_curiosity_delta_is_zero_exact_mi_is_not():
    p, q_bar = 0.70, 0.78
    lo = valid_channel(p, 0.70, q_bar)
    hi = valid_channel(p, 0.85, q_bar)
    assert lo is not None and hi is not None
    target = min(lo.gross_classification_value(), hi.gross_classification_value())
    lo, hi = cost_match(lo, target), cost_match(hi, target)
    assert lo.mean_accuracy() == pytest.approx(hi.mean_accuracy())
    assert lo.instrumental_sample_value() == pytest.approx(hi.instrumental_sample_value())
    assert abs(hi.mutual_information_nats() - lo.mutual_information_nats()) > 0.05
    bonus = curiosity_bonus(p, q_bar, kappa=1.0, gamma=2.0)
    d_cur = abs(hi.policy(bonus)[3] - lo.policy(bonus)[3])
    d_mi = abs(
        hi.policy(hi.mutual_information_nats())[3] - lo.policy(lo.mutual_information_nats())[3]
    )
    assert d_cur < 1e-9
    assert d_mi > 0.05
    assert abs(hi.ambiguity_nats() - lo.ambiguity_nats()) > 1e-4
    d_i = hi.mutual_information_nats() - lo.mutual_information_nats()
    d_h = (hi.mutual_information_nats() + hi.ambiguity_nats()) - (
        lo.mutual_information_nats() + lo.ambiguity_nats()
    )
    d_a = hi.ambiguity_nats() - lo.ambiguity_nats()
    assert d_i == pytest.approx(d_h - d_a)
