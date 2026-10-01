import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from eqr_symmetric_audit import (  # noqa: E402
    compile_matrix,
    controllers,
    max_abs_distance,
    probes,
)


def test_rename_is_exact_gauge():
    names = [n for n, _ in controllers()]
    dist = max_abs_distance(compile_matrix(names, probes()))
    i = names.index("exact_mi_a1_b8")
    j = names.index("exact_mi_a1_b8_copy")
    assert dist[i, j] <= 1e-12


def test_instrumental_is_not_exact_mi_on_this_probe_algebra():
    names = [n for n, _ in controllers()]
    dist = max_abs_distance(compile_matrix(names, probes()))
    i = names.index("instr_b8")
    j = names.index("exact_mi_a1_b8")
    assert dist[i, j] > 0.05
