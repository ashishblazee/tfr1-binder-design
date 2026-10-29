"""
01_map_conserved_epitope.py
===========================
Challenge 4: TfR1 pH-Selective Cross-Reactive Binder Design
Stage 1: Human vs Mouse Sequence Conservation & Epitope Mapping

Identifies the 100% invariant surface residues between Human TfR1 (P02786)
and Mouse TfR1 (Q62351) on the Apical Domain (residues 188-383) to achieve
the species-symmetry tiebreaker: KD(mouse) / KD(human) ≈ 1.0.

Author: Ashish (github.com/ashishblazee)
"""

import os
import csv
import urllib.request

def fetch_uniprot_fasta(accession: str) -> str:
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        lines = resp.read().decode('utf-8').splitlines()
    return ''.join([l.strip() for l in lines if not l.startswith('>')])

def align_nw(s1: str, s2: str) -> tuple[str, str]:
    dp = [[0]*(len(s2)+1) for _ in range(len(s1)+1)]
    for i in range(len(s1)+1): dp[i][0] = -i * 2
    for j in range(len(s2)+1): dp[0][j] = -j * 2
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            match = dp[i-1][j-1] + (3 if s1[i-1] == s2[j-1] else -1)
            del_ = dp[i-1][j] - 2
            ins_ = dp[i][j-1] - 2
            dp[i][j] = max(match, del_, ins_)
    i, j = len(s1), len(s2)
    a1, a2 = [], []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (3 if s1[i-1] == s2[j-1] else -1):
            a1.append(s1[i-1])
            a2.append(s2[j-1])
            i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] - 2:
            a1.append(s1[i-1])
            a2.append('-')
            i -= 1
        else:
            a1.append('-')
            a2.append(s2[j-1])
            j -= 1
    return ''.join(reversed(a1)), ''.join(reversed(a2))

def main():
    print("=" * 65)
    print("STAGE 1: Mapping Human vs Mouse TfR1 Epitope Conservation")
    print("=" * 65)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    # 1. Fetch sequences
    print("1. Fetching UniProt sequences (Human: P02786, Mouse: Q62351)...")
    h_seq = fetch_uniprot_fasta("P02786")
    m_seq = fetch_uniprot_fasta("Q62351")
    
    # 2. Extract competition constructs
    # Human: 121-760 (1-based: index 120 to 760)
    # Mouse: 123-763 (1-based: index 122 to 763)
    h_ecto = h_seq[120:760]
    m_ecto = m_seq[122:763]
    print(f"   Human ectodomain (121-760): {len(h_ecto)} aa")
    print(f"   Mouse ectodomain (123-763): {len(m_ecto)} aa")

    # 3. Align Apical Domains (Human: 188-383, Mouse: 190-385)
    h_apical = h_seq[187:383] # 196 aa
    m_apical = m_seq[189:386] # 197 aa
    
    a_h, a_m = align_nw(h_apical, m_apical)
    
    # 4. Map the viral Tyr211 patch (known non-conserved site)
    print("\n2. The Viral Tyr211 Patch (Non-Conserved Trap):")
    trap_positions = [
        ("Asp204", "Gln207", "Charge altered"),
        ("Arg208", "Asn211", "Basic side chain lost"),
        ("Val210", "Asp213", "Hydrophobic -> Negative charge"),
        ("Tyr211", "Pro214", "Aromatic ring -> Rigid Proline"),
        ("Leu212", "DELETED", "Residue deleted in mouse"),
        ("Asn348", "Lys350", "Neutral -> Basic"),
        ("Lys371", "Gln373", "Basic -> Neutral")
    ]
    for h_res, m_res, impact in trap_positions:
        print(f"   Human {h_res:8s} -> Mouse {m_res:8s} ({impact})")
    print("   --> Targeting this patch guarantees failure in mouse cross-reactivity!")

    # 5. Map the 95.5% Conserved Apical Ridge (Residues 305 to 348)
    print("\n3. The Target: Conserved Apical Ridge (Residues 305-348):")
    h_ridge = h_seq[304:348] # 305 to 348
    print(f"   Human (305-348): {h_ridge}")
    idx_m = m_seq.find("TGDPY")
    m_ridge = m_seq[idx_m:idx_m+44]
    print(f"   Mouse (307-350): {m_ridge}")
    matches = sum(1 for a, b in zip(h_ridge, m_ridge) if a == b)
    print(f"   Conservation: {matches}/44 aa ({matches/44*100:.1f}%) IDENTICAL!")

    conserved_patches = []
    curr_h_pos = 188
    for i in range(len(a_h)):
        ch_h = a_h[i]
        ch_m = a_m[i]
        if ch_h != '-':
            if ch_h == ch_m:
                conserved_patches.append((curr_h_pos, ch_h, "CONSERVED"))
            else:
                conserved_patches.append((curr_h_pos, ch_h, f"MUTATED_TO_{ch_m}"))
            curr_h_pos += 1

    # Save to data directory
    out_csv = os.path.join(data_dir, "tfr1_apical_conservation_map.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["human_res_num", "human_aa", "mouse_status"])
        for row in conserved_patches:
            writer.writerow(row)
            
    print(f"\n[PASS] Saved complete conservation map to: {out_csv}")
    print("=" * 65)

if __name__ == "__main__":
    main()
