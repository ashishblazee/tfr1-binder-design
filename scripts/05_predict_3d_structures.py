"""
Script 05: Predict 3D Structures of Top Candidates via ESMFold
--------------------------------------------------------------
Queries the ESMFold API (Meta AI) to predict all-atom 3D coordinates
and residue-level pLDDT confidence scores for top TfR1 binder designs.
Saves .pdb structures to structures/ directory and extracts pLDDT metrics.
"""

import os
import time
import urllib.request
import pandas as pd

ESMFOLD_URL = "https://api.esmatlas.com/foldSequence/v1/pdb/"

def fold_sequence(seq, name, out_dir):
    pdb_path = os.path.join(out_dir, f"{name}.pdb")
    if os.path.exists(pdb_path) and os.path.getsize(pdb_path) > 1000:
        print(f"[CACHE] {name} already folded at {pdb_path}")
        return pdb_path, extract_mean_plddt(pdb_path)
        
    print(f"[FOLDING] Sending {name} ({len(seq)} aa) to ESMFold...")
    req = urllib.request.Request(
        ESMFOLD_URL,
        data=seq.encode("utf-8"),
        headers={"Content-Type": "text/plain", "User-Agent": "TfR1-Design-Bot/1.0"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 200:
                pdb_content = resp.read().decode("utf-8")
                with open(pdb_path, "w", encoding="utf-8") as f:
                    f.write(pdb_content)
                mean_plddt = extract_mean_plddt(pdb_path)
                print(f"[PASS] Successfully folded {name}! Mean pLDDT: {mean_plddt:.1f}")
                return pdb_path, mean_plddt
            else:
                print(f"[FAIL] HTTP error {resp.status} for {name}")
                return None, 0.0
    except Exception as e:
        print(f"[FAIL] Error folding {name}: {e}")
        return None, 0.0

def extract_mean_plddt(pdb_path):
    plddts = []
    with open(pdb_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                try:
                    # B-factor column in ESMFold holds pLDDT (0 - 100)
                    b_factor = float(line[60:66].strip())
                    plddts.append(b_factor)
                except ValueError:
                    pass
    if plddts:
        return sum(plddts) / len(plddts)
    return 0.0

def main():
    sub_path = os.path.join(os.path.dirname(__file__), "..", "data", "proteinbase_submission_tfr1.csv")
    df = pd.read_csv(sub_path)
    
    out_dir = os.path.join(os.path.dirname(__file__), "..", "structures")
    os.makedirs(out_dir, exist_ok=True)
    
    # Fold all 20 designs in the portfolio
    top_designs = df
    
    results = []
    for idx, row in top_designs.iterrows():
        name = row["name"]
        seq = row["sequence"]
        pdb_file, mean_plddt = fold_sequence(seq, name, out_dir)
        results.append({
            "rank": row["rank"],
            "name": name,
            "molecule_class": row["molecule_class"],
            "length": len(seq),
            "mean_plddt": round(mean_plddt, 1),
            "pdb_file": pdb_file
        })
        time.sleep(1.0) # gentle rate limit
        
    df_results = pd.DataFrame(results)
    out_summary = os.path.join(os.path.dirname(__file__), "..", "data", "top_structures_plddt.csv")
    df_results.to_csv(out_summary, index=False)
    print("\n--- 3D FOLDING VALIDATION SUMMARY ---")
    print(df_results.to_string(index=False))

if __name__ == "__main__":
    main()
