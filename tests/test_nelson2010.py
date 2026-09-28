from nelson2010 import F, G, assert_paper_claims, condition1_table


def test_probability_gain_tied():
    assert abs(F.probability_gain() - 0.25) < 1e-12
    assert abs(G.probability_gain() - 0.25) < 1e-12


def test_accuracy_tied():
    assert abs(F.expected_accuracy() - 0.75) < 1e-12
    assert abs(G.expected_accuracy() - 0.75) < 1e-12


def test_f_has_higher_mi():
    assert F.mutual_information_nats() > G.mutual_information_nats()
    assert abs(F.mutual_information_nats() - 0.2158) < 5e-4
    assert abs(G.mutual_information_nats() - 0.1308) < 5e-4


def test_paper_claim_bundle():
    assert_paper_claims()
    rows = {r["channel"]: r for r in condition1_table()}
    assert rows["F"]["probability_gain"] == rows["G"]["probability_gain"]
