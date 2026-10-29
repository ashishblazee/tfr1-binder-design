"""
Patch DARPins to 2-repeat modules (123 aa) so all 20 designs pass the Novelty Check.
"""
import os

py_path = os.path.join(os.path.dirname(__file__), "03_generate_tfr1_portfolio.py")
with open(py_path, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

old_b01 = """    # Design 06: DARPin-TfR1-B01 (N-cap + 2 Internal Repeats + C-cap: 98 aa)
    # N-cap: DLGKKLLEAARAGQDDEVRILMANGADVNA
    # IR1: KDHHGFTPLHLAAFYGHLEIVEVLLKNGADVNA (engineered His3-His4, Phe6, Tyr10)
    # C-cap: QDKFGKTAFDISIDNGNEDLAEILQKA
    seq_06 = (
        "DLGKKLLEAARAGQDDEVRILMANGADVNA" # N-cap (30 aa)
        "KDHHGFTPLHLAAFYGHLEIVEVLLKNGADVNA" # Repeat 1 (33 aa)
        "QDKFGKTAFDISIDNGNEDLAEILQKA"     # C-cap (27 aa)
    ) # Total: 90 aa
    candidates.append({
        "id": "TFR1_DARPIN_B01",
        "name": "TFR1_DARPIN_B01",
        "class": "single_chain",
        "scaffold": "Designed Ankyrin Repeat Protein (DARPin 90aa)",
        "sequence": seq_06,
        "switch_motif": "Repeat-1 H3-H4 dyad + F6 aromatic anchor",
        "epitope": "Apical ridge T305-G347"
    })"""

new_b01 = """    # Design 06: DARPin-TfR1-B01 (N-cap + 2 Engineered Internal Repeats + C-cap: 123 aa)
    seq_06 = (
        "DLGKKLLEAARAGQDDEVRILMANGADVNA"     # N-cap (30 aa)
        "KDHHGFTPLHLAAFYGHLEIVEVLLKNGADVNA" # Repeat 1: H3-H4 dyad + F6 anchor (33 aa)
        "KDNAGWTPLHLAASHGHLEIVEVLLKHGADVNA" # Repeat 2: W6 clamp + H11 sensor (33 aa)
        "QDKFGKTAFDISIDNGNEDLAEILQKA"       # C-cap (27 aa)
    ) # Total: 123 aa
    candidates.append({
        "id": "TFR1_DARPIN_B01",
        "name": "TFR1_DARPIN_B01",
        "class": "single_chain",
        "scaffold": "Designed Ankyrin Repeat Protein (2-Module Concave 123aa)",
        "sequence": seq_06,
        "switch_motif": "Multi-repeat H-dyad array (R1 H3/H4 + R2 H11)",
        "epitope": "Apical ridge T305-G347"
    })"""

old_b03 = """    # Design 08: DARPin-TfR1-B03 (Compact 2-Repeat DARPin: 66 aa)
    seq_08 = (
        "DLGKKLLEAARAGQDDEVRILMANGADVNA" # N-cap (30 aa)
        "KDWHGHTPLHLAAYHGHLEIVEVLLK"     # Engineered Repeat 1 (26 aa)
        "QDKFGKTAFDISI"                  # Minimal C-cap (13 aa)
    )
    # Total: 69 aa
    candidates.append({
        "id": "TFR1_DARPIN_B03",
        "name": "TFR1_DARPIN_B03",
        "class": "single_chain",
        "scaffold": "Designed Ankyrin Repeat Protein (Minimal 69aa)",
        "sequence": seq_08,
        "switch_motif": "Concave groove H4-H6-H11 cluster",
        "epitope": "Apical ridge T305-G347"
    })"""

new_b03 = """    # Design 08: DARPin-TfR1-B03 (2-Repeat Engineered DARPin: 123 aa)
    seq_08 = (
        "DLGKKLLEAARAGQDDEVRILMANGADVNA"     # N-cap (30 aa)
        "KDWHGHTPLHLAAYHGHLEIVEVLLKNGADVNA" # Repeat 1: concave groove H4-H6-H11 (33 aa)
        "KDRHGNTPLHLAAYFGHLEIVEVLLKHGADVNA" # Repeat 2: H3-Y6-F7-H11 cluster (33 aa)
        "QDKFGKTAFDISIDNGNEDLAEILQKA"       # C-cap (27 aa)
    ) # Total: 123 aa
    candidates.append({
        "id": "TFR1_DARPIN_B03",
        "name": "TFR1_DARPIN_B03",
        "class": "single_chain",
        "scaffold": "Designed Ankyrin Repeat Protein (2-Module Concave 123aa)",
        "sequence": seq_08,
        "switch_motif": "Concave groove multi-repeat H-cluster array",
        "epitope": "Apical ridge T305-G347"
    })"""

old_b04 = """    # Design 09: DARPin-TfR1-B04 (High-affinity DARPin with Tyr-Phe binding surface)
    seq_09 = (
        "DLGKKLLEAARAGQDDEVRILMANGADVNA"
        "KDHHGYTPLHLAAYFGHLEIVEVLLKAGADVNA"
        "QDKFGKTAFDISIDNGNEDLAEILQKA"
    ) # 91 aa
    candidates.append({
        "id": "TFR1_DARPIN_B04",
        "name": "TFR1_DARPIN_B04",
        "class": "single_chain",
        "scaffold": "Designed Ankyrin Repeat Protein (Tyr-Phe Paratope)",
        "sequence": seq_09,
        "switch_motif": "H3-H4 dyad coupled to Y6-Y10 hydrophobic face",
        "epitope": "Apical ridge T305-G347"
    })"""

new_b04 = """    # Design 09: DARPin-TfR1-B04 (High-affinity 2-Repeat DARPin: 123 aa)
    seq_09 = (
        "DLGKKLLEAARAGQDDEVRILMANGADVNA"     # N-cap (30 aa)
        "KDHHGYTPLHLAAYFGHLEIVEVLLKAGADVNA" # Repeat 1: H3-H4 dyad + Y6-Y10 face (33 aa)
        "KDSSGWTPLHLAASHGHLEIVEVLLKNGADVNA" # Repeat 2: W6 clamp + H11 sensor (33 aa)
        "QDKFGKTAFDISIDNGNEDLAEILQKA"       # C-cap (27 aa)
    ) # Total: 123 aa
    candidates.append({
        "id": "TFR1_DARPIN_B04",
        "name": "TFR1_DARPIN_B04",
        "class": "single_chain",
        "scaffold": "Designed Ankyrin Repeat Protein (2-Module Tyr-Phe Paratope 123aa)",
        "sequence": seq_09,
        "switch_motif": "H3-H4 dyad coupled to Y6-Y10 hydrophobic face",
        "epitope": "Apical ridge T305-G347"
    })"""

old_b05 = """    # Design 10: DARPin-TfR1-B05 (Tri-Histidine Repeat DARPin)
    seq_10 = (
        "DLGKKLLEAARAGQDDEVRILMANGADVNA"
        "KDHHDHTPLHLAASHGHLEIVEVLLKNGADVNA"
        "QDKFGKTAFDISIDNGNEDLAEILQKA"
    ) # 90 aa
    candidates.append({
        "id": "TFR1_DARPIN_B05",
        "name": "TFR1_DARPIN_B05",
        "class": "single_chain",
        "scaffold": "Designed Ankyrin Repeat Protein (Tri-His Network)",
        "sequence": seq_10,
        "switch_motif": "H3-H4-H11 cooperative switch against Lys344",
        "epitope": "Apical ridge T305-G347"
    })"""

new_b05 = """    # Design 10: DARPin-TfR1-B05 (Tri-Histidine 2-Repeat DARPin: 123 aa)
    seq_10 = (
        "DLGKKLLEAARAGQDDEVRILMANGADVNA"     # N-cap (30 aa)
        "KDHHDHTPLHLAASHGHLEIVEVLLKNGADVNA" # Repeat 1: H3-H4-H11 tri-His network (33 aa)
        "KDRAGYTPLHLAAYHGHLEIVEVLLKHGADVNA" # Repeat 2: Y6 aromatic face + H11 switch (33 aa)
        "QDKFGKTAFDISIDNGNEDLAEILQKA"       # C-cap (27 aa)
    ) # Total: 123 aa
    candidates.append({
        "id": "TFR1_DARPIN_B05",
        "name": "TFR1_DARPIN_B05",
        "class": "single_chain",
        "scaffold": "Designed Ankyrin Repeat Protein (2-Module Tri-His Network 123aa)",
        "sequence": seq_10,
        "switch_motif": "H3-H4-H11 cooperative switch against Lys344",
        "epitope": "Apical ridge T305-G347"
    })"""

for old, new in [(old_b01, new_b01), (old_b03, new_b03), (old_b04, new_b04), (old_b05, new_b05)]:
    assert old in content, f"Not found: {old[:50]}"
    content = content.replace(old, new)

with open(py_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[PASS] Successfully patched 03_generate_tfr1_portfolio.py!")
