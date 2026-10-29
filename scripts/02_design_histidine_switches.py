"""
Script 02: Design Histidine Switches for pH-Selective TfR1 Binding
-------------------------------------------------------------------
This script models the cooperative electrostatic repulsion switch mechanism.
Rule:
At pH 7.4 (blood plasma):
  - Histidines (pKa ~6.2-6.5) are predominantly uncharged (~94% neutral).
  - Aromatic imidazole rings pack against hydrophobic patches on TfR1 (Phe313, Phe316, Phe321, Leu345).
  - Kd is sub-micromolar / nanomolar against both Human and Mouse TfR1.

At pH 6.0 (early endosome):
  - Histidines become protonated (His+ carrying a +1 net charge).
  - Interfacial His residues positioned adjacent to:
      1) TfR1 basic residues: Arg339 (+1), Lys344 (+1)
      2) Other binder His residues (His-His repulsive dyads/triads, < 5 Angstroms apart)
  - Result: Severe electrostatic repulsion (+1 vs +1) + desolvation penalty.
  - Delta G_binding shifts positive, completely abolishing binding (Kd > 100 uM, "no detectable binding").

The script exports quantitative switch profiles and optimal histidine placement motifs.
"""

import math
import os
import pandas as pd

def calculate_protonation_fraction(pH, pKa=6.2):
    """Henderson-Hasselbalch equation for Histidine protonation fraction."""
    # pH = pKa + log10([Base]/[Acid])
    # [Acid]/[Total] = 1 / (1 + 10^(pH - pKa))
    return 1.0 / (1.0 + 10.0 ** (pH - pKa))

def calculate_electrostatic_repulsion(q1, q2, distance_angstrom=4.0, dielectric=40.0):
    """
    Coulomb electrostatic energy in kcal/mol:
    E = (332 / eps) * (q1 * q2 / r)
    dielectric in protein interface ~ 20 - 40
    """
    if distance_angstrom <= 0:
        return 0.0
    return (332.0 / dielectric) * (q1 * q2 / distance_angstrom)

def evaluate_switch_architecture():
    results = []
    
    # 1 His vs 1 His, 2 His cluster, 3 His cooperative triad
    configs = [
        {"name": "Single His (Baseline)", "num_his": 1, "target_counterpart": "Arg339 (+1)", "q_tfr1": 1.0},
        {"name": "His-His Dyad vs Arg339", "num_his": 2, "target_counterpart": "Arg339 (+1)", "q_tfr1": 1.0},
        {"name": "His-His Dyad vs Lys344", "num_his": 2, "target_counterpart": "Lys344 (+1)", "q_tfr1": 1.0},
        {"name": "Cooperative His Triad vs Arg339/Lys344", "num_his": 3, "target_counterpart": "Arg339 + Lys344 (+2)", "q_tfr1": 2.0},
    ]
    
    for cfg in configs:
        f_74 = calculate_protonation_fraction(7.4, pKa=6.3)
        f_60 = calculate_protonation_fraction(6.0, pKa=6.3)
        
        # Net charge on binder His cluster at pH 7.4 and 6.0
        q_binder_74 = cfg["num_his"] * f_74
        q_binder_60 = cfg["num_his"] * f_60
        
        e_rep_74 = calculate_electrostatic_repulsion(q_binder_74, cfg["q_tfr1"], distance_angstrom=4.2, dielectric=35.0)
        e_rep_60 = calculate_electrostatic_repulsion(q_binder_60, cfg["q_tfr1"], distance_angstrom=4.2, dielectric=35.0)
        
        delta_e = e_rep_60 - e_rep_74
        
        # Theoretical Kd shift fold = exp(delta_E / RT) where RT ~ 0.593 kcal/mol at 298K
        kd_fold_drop = math.exp(delta_e / 0.593)
        
        # Status
        passes_gate = "EXCELLENT (Complete Shutoff)" if kd_fold_drop >= 500 else ("MODERATE (Risk of Residual Binding)" if kd_fold_drop >= 50 else "INSUFFICIENT")
        
        results.append({
            "Architecture": cfg["name"],
            "Num Interfacial His": cfg["num_his"],
            "Target Counterpart": cfg["target_counterpart"],
            "Repulsion pH 7.4 (kcal/mol)": round(e_rep_74, 2),
            "Repulsion pH 6.0 (kcal/mol)": round(e_rep_60, 2),
            "Delta G Repulsion (kcal/mol)": round(delta_e, 2),
            "Theoretical Fold Kd Drop": round(kd_fold_drop, 1),
            "Competition Gate 2 Status": passes_gate
        })
        
    df = pd.DataFrame(results)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "histidine_switch_modeling.csv")
    df.to_csv(out_path, index=False)
    print(f"[PASS] Saved histidine switch modeling to {out_path}")
    print(df.to_string(index=False))

if __name__ == "__main__":
    evaluate_switch_architecture()
