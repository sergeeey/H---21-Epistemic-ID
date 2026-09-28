#!/usr/bin/env python3
"""Generate the 2-page outreach research brief. No new experimental results."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outreach" / "Structural_Identifiability_Matched_Channel_Research_Brief_v1.1.pdf"

NAVY = colors.HexColor("#1F3A5F")
RULE = colors.HexColor("#C5CDD6")
BOX = colors.HexColor("#EEF3F8")
HEAD = colors.HexColor("#1F3A5F")


def styles():
    base = getSampleStyleSheet()
    s = {
        "title": ParagraphStyle(
            "TitleX",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=13.5,
            leading=16,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=3,
        ),
        "subtitle": ParagraphStyle(
            "SubX",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=10.5,
            leading=13,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "meta": ParagraphStyle(
            "MetaX",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#555555"),
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "status": ParagraphStyle(
            "StatX",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=8,
            leading=10,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "h": ParagraphStyle(
            "HX",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=10.5,
            leading=13,
            textColor=NAVY,
            spaceBefore=7,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "BX",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=9.2,
            leading=11.6,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "SX",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            leading=10.2,
            alignment=TA_JUSTIFY,
            spaceAfter=2,
        ),
        "cell": ParagraphStyle(
            "CX",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=7.4,
            leading=9.4,
            alignment=TA_LEFT,
        ),
        "cellh": ParagraphStyle(
            "CH",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=7.4,
            leading=9.4,
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
        "box": ParagraphStyle(
            "BoxX",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=8.4,
            leading=10.8,
            alignment=TA_LEFT,
            textColor=NAVY,
        ),
        "foot": ParagraphStyle(
            "FX",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=7.5,
            leading=9,
            textColor=colors.HexColor("#555555"),
            alignment=TA_CENTER,
        ),
    }
    return s


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(
        0.7 * inch, letter[1] - 0.48 * inch, letter[0] - 0.7 * inch, letter[1] - 0.48 * inch
    )
    canvas.setFont("Times-Italic", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(0.7 * inch, letter[1] - 0.40 * inch, "Research brief  ·  Version 1.1")
    canvas.drawRightString(
        letter[0] - 0.7 * inch, letter[1] - 0.40 * inch, "Confidential circulation"
    )
    canvas.line(0.7 * inch, 0.48 * inch, letter[0] - 0.7 * inch, 0.48 * inch)
    canvas.drawCentredString(
        letter[0] / 2,
        0.32 * inch,
        f"METHOD PROPOSED  ·  page {doc.page} of 2  ·  Internal ID: AIF-KILL-001",
    )
    canvas.restoreState()


def pcell(text, style):
    return Paragraph(text, style)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.62 * inch,
        title="Structural Identifiability of Epistemic Value in Active Inference",
        author="Research brief v1.1",
        subject="Matched-channel experimental design — METHOD PROPOSED",
    )
    story = []
    story.append(
        Paragraph(
            "Structural Identifiability of Epistemic Value in Active Inference",
            s["title"],
        )
    )
    story.append(
        Paragraph(
            "A Matched-Channel Experimental Design",
            s["subtitle"],
        )
    )
    story.append(
        Paragraph(
            "Research brief · Version 1.1 · 28 September 2026",
            s["meta"],
        )
    )
    story.append(
        Paragraph(
            "METHOD PROPOSED  +  SYNTHETICALLY IDENTIFIABLE  +  HUMAN VALIDATION PENDING",
            s["status"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))

    story.append(Paragraph("1. The identifiability problem", s["h"]))
    story.append(
        Paragraph(
            "Active Inference (AIF) scores policies by expected free energy, which decomposes into a pragmatic "
            "term and an epistemic expected-information-gain term. Observing information-seeking choices does "
            "not identify that decomposition. Intrinsic-motivation models, Bayesian experimental design, "
            "information-directed sampling, and several human question-selection utilities can produce similar "
            "sampling. The relevant competitor class is therefore not merely reward-based reinforcement "
            "learning, but <b>alternative information-seeking objectives</b>.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "We study a reduced one-step controller derived from expected free energy under stated assumptions "
            "(binary hidden state, finite observations, one-step sampling, fixed preferences, Bayesian updating). "
            "The reduced score is <i>V</i> = <i>V</i><sub>instr</sub> + α<sub>epi</sub> <i>I</i>(<i>Z</i>; <i>Y</i>). "
            "This tests an EFE-derived epistemic-value component. It does not test the entirety of Active Inference. "
            "The intended ladder is general FEP → specific EFE/AIF model → identifiable prediction → strong rival. "
            "This note occupies only the last two rungs.",
            s["body"],
        )
    )

    story.append(Paragraph("2. Why ordinary tasks fail (v4–v5)", s["h"]))
    story.append(
        Paragraph(
            "Reward-only and flexible Bayes-adaptive instrumental rivals were separable when the epistemic "
            "weight was strong. A generic curiosity bonus of a different functional form, "
            "<i>V</i><sub>curiosity</sub> = <i>V</i><sub>instr</sub> + κ <i>H</i>(<i>Z</i>)(2<i>q</i>−1)<sup>γ</sup>, "
            "destroyed that specificity. In the tested symmetric-cue grid the median minimum Jensen–Shannon "
            "divergence was approximately 5.5×10<sup>−7</sup> (90th percentile ≈ 5.9×10<sup>−6</sup>; "
            "maximum ≈ 2×10<sup>−5</sup>). A search over 175,821 symmetric-cue pairs found no fully robust "
            "sign-reversal discriminator; the best pair reversed the ordering for about 71.8% of tested "
            "curiosity parameterizations. Information seeking, as such, is not mechanism-specific.",
            s["body"],
        )
    )

    story.append(Paragraph("3. Proposed solution: matched asymmetric channels (v6)", s["h"]))
    story.append(
        Paragraph(
            "We propose a matched-channel design. Sensitivity <i>a</i> = P(<i>Y</i>=L|<i>Z</i>=L) and "
            "specificity <i>b</i> = P(<i>Y</i>=R|<i>Z</i>=R) replace a single reliability <i>q</i>. "
            "Selected pairs hold constant the prior, mean cue accuracy, and instrumental sampling value, "
            "while varying exact mutual information <i>I</i>(<i>Z</i>; <i>Y</i>). An exact-MI controller then "
            "predicts a sizable within-pair sampling contrast; the tested accuracy-based curiosity family "
            "predicts approximately none. <i>v6 discriminates the tested curiosity family; it does not "
            "discriminate all conceivable information-seeking algorithms</i>. This design class is not new: "
            "Nelson et al. (2010, E3 C1) already tied probability gain (0.25) while varying information gain "
            "(I ≈ 0.2158 vs 0.1308 nats); only 12/22 humans preferred the richer channel. v6 is an "
            "AIF-framed analogue, not a first discriminator.",
            s["body"],
        )
    )

    header = [
        pcell(h, s["cellh"])
        for h in [
            "Pair",
            "Prior p",
            "Mean acc.",
            "ΔMI (nats)",
            "Pred. ΔP exact-MI",
            "Pred. ΔP curiosity",
        ]
    ]
    rows = [header]
    for row in [
        ["1", "0.70", "0.780", "0.143", "0.277", "0"],
        ["2", "0.80", "0.846", "0.138", "0.270", "2.22×10−16"],
        ["3", "0.70", "0.738", "0.140", "0.259", "0"],
        ["4", "0.80", "0.798", "0.136", "0.245", "0"],
    ]:
        rows.append([pcell(c, s["cell"]) for c in row])
    table = Table(
        rows,
        colWidths=[0.55 * inch, 0.85 * inch, 0.95 * inch, 1.05 * inch, 1.35 * inch, 1.35 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEAD),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#F4F7FA")),
                ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#F4F7FA")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("GRID", (0, 0), (-1, -1), 0.3, RULE),
            ]
        )
    )
    story.append(table)
    story.append(
        Paragraph(
            "Table 1. Candidate matched pairs (synthetic predictions). At 240 synthetic trials, family recovery "
            "was 98.3% (exact-MI) and 96.7% (tested curiosity). These toy rates must not be used to choose "
            "participant N.",
            s["small"],
        )
    )

    story.append(Paragraph("4. Interpretation ceiling (v7)", s["h"]))
    story.append(
        Paragraph(
            "If another controller implements the same exact-MI objective and the same policy mapping, "
            "Q<sub>1</sub>(<i>a</i>|<i>x</i>) = Q<sub>2</sub>(<i>a</i>|<i>x</i>) for every action and condition. "
            "A numerical grid check returned zero difference to floating-point precision. The equivalence "
            "result is not a mathematically surprising theorem; it delimits interpretation. A later positive "
            "human contrast can support exact-MI-sensitive valuation relative to specified alternatives. "
            "It cannot uniquely identify Active Inference or the Free Energy Principle.",
            s["body"],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("5. What is needed next: a human feasibility pilot", s["h"]))
    story.append(
        Paragraph(
            "The bottleneck is no longer toy-model separability. It is whether participants can learn "
            "asymmetric contingencies well enough for the contrast to survive. Three risks cannot be settled "
            "in simulation: (R1) failure to learn <i>a</i> and <i>b</i>; (R2) between-subject heterogeneity "
            "that attenuates the contrast; (R3) simple heuristics that reproduce the signature. A pilot should "
            "estimate learnability, interface comprehension, empirical variance, subjective estimates of "
            "<i>a</i> and <i>b</i>, sampling-rate floor/ceiling, and candidate heuristics. It is a "
            "feasibility study, not a confirmatory test. Final N and decision thresholds will be set only "
            "after hierarchical simulation-based calibration (planned v9; not yet run).",
            s["body"],
        )
    )

    box_data = [
        [
            Paragraph(
                "Ask. I can contribute the design, reduced models, and adversarial comparison pipeline. "
                "I am looking for a collaborator with human behavioral-experiment infrastructure to "
                "co-develop a small feasibility pilot and, if warranted, later freeze a preregistered "
                "confirmatory protocol. The first question is not “is FEP true?” but: "
                "<b>how do we experimentally distinguish exact information gain from merely generic information-seeking?</b>",
                s["box"],
            )
        ]
    ]
    box = Table(box_data, colWidths=[7.1 * inch])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BOX),
                ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(Spacer(1, 4))
    story.append(KeepTogether([box]))
    story.append(Spacer(1, 6))

    role_header = [
        pcell(h, s["cellh"]) for h in ["This side can contribute", "Sought from a collaborator"]
    ]
    role_rows = [role_header]
    for left, right in [
        [
            "Matched-channel task geometry; reduced EFE mapping; adversarial v1–v7 sequence",
            "Judgment of human learnability and interface for asymmetric cues",
        ],
        [
            "Simulation code for the shipped v1 checks; preprint and this brief",
            "Recruitment, ethics / IRB pathway, and local experimental expertise",
        ],
        [
            "A planned hierarchical calibration (v9) before any confirmatory N is frozen",
            "Joint interpretation; later, if warranted, a frozen confirmatory protocol",
        ],
    ]:
        role_rows.append([pcell(left, s["cell"]), pcell(right, s["cell"])])
    roles = Table(role_rows, colWidths=[3.55 * inch, 3.55 * inch])
    roles.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEAD),
                ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#F4F7FA")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.3, RULE),
            ]
        )
    )
    story.append(roles)
    story.append(
        Paragraph(
            "Table 2. Proposed division of labor for a conversation, not a frozen authorship agreement.",
            s["small"],
        )
    )

    story.append(Paragraph("6. What this brief does not claim", s["h"]))
    story.append(
        Paragraph(
            "No “first” or “breakthrough” claim is made. Design-class novelty is not supported given Nelson et al. "
            "2010. No new human data have been collected here. The current protocol is "
            "preregistration-<b>oriented</b>, not preregistration-ready. Entropies in the simulations are in "
            "nats: for <i>p</i>=0.64, <i>q</i>=0.95, <i>I</i>(<i>Z</i>;<i>Y</i>)≈0.4625 nats "
            "(a value near 0.953 is bits). Available now: preprint v1.1, this brief, and a one-command "
            "reproduction of the v1 mutual-information and reward-only discrimination checks. The full "
            "v4–v8 search pipeline is documented in the preprint and is not yet shipped as a public "
            "end-to-end script.",
            s["body"],
        )
    )
    story.append(
        Paragraph(
            "Selected references: Friston et al., Cogn Neurosci 2015; Da Costa et al., J Math Psychol 2020; "
            "Smith, Friston &amp; Whyte, J Math Psychol 2022; Chou et al., J Math Psychol 2026; "
            "Nelson, Psychol Rev 2005; Russo &amp; Van Roy, NeurIPS 2014.",
            s["foot"],
        )
    )

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    from pypdf import PdfReader

    n = len(PdfReader(str(OUT)).pages)
    print("wrote", OUT, "pages", n)
    if n != 2:
        raise SystemExit(f"Brief must be exactly 2 pages, got {n}")


if __name__ == "__main__":
    build()
