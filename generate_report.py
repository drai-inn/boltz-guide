import base64
import json
import os

import numpy as np
import yaml

ROOT = "/home/rche591/boltz-guide"
EXP = "boltz-02"
TEMPLATE = os.path.join(ROOT, "boltz_results_boltz-01", "report.html")
OUTPUT = os.path.join(ROOT, f"boltz_results_{EXP}", "report.html")
PRED_DIR = os.path.join(ROOT, f"boltz_results_{EXP}", "predictions", EXP)
RESULTS_DIR = os.path.join(ROOT, f"boltz_results_{EXP}")

with open(TEMPLATE) as f:
    html = f.read()

with open(os.path.join(PRED_DIR, f"{EXP}_model_0.cif")) as f:
    cif = f.read()

plddt = np.load(os.path.join(PRED_DIR, f"plddt_{EXP}_model_0.npz"))["plddt"].flatten()
pae = np.load(os.path.join(PRED_DIR, f"pae_{EXP}_model_0.npz"))["pae"]
with open(os.path.join(PRED_DIR, f"confidence_{EXP}_model_0.json")) as f:
    conf = json.load(f)

with open(os.path.join(ROOT, f"{EXP}.yaml")) as f:
    cfg = yaml.safe_load(f)

protein_seq = cfg["sequences"][1]["protein"]["sequence"]
smiles = cfg["sequences"][0]["ligand"]["smiles"]
aa_count = len(protein_seq)
ligand_n = len(plddt) - aa_count
dim = int(pae.shape[0])
assert pae.shape == (dim, dim) and dim == len(plddt), f"dimension mismatch: pae={pae.shape}, plddt={len(plddt)}"
assert ligand_n > 0 and ligand_n < 20

pae_max = float(pae.max())
pae_cap = round(pae_max + 0.25, 2)
pae_u8 = np.clip(np.round(pae / pae_cap * 255), 0, 255).astype(np.uint8)
pae_b64 = base64.b64encode(pae_u8.tobytes()).decode()

manifest = []
for dirpath, _, filenames in os.walk(RESULTS_DIR):
    for fn in sorted(filenames):
        if fn == "report.html":
            continue
        manifest.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
manifest.sort()


def rep(old, new):
    global html
    assert html.count(old) == 1, f"pattern not unique/missing: {old[:80]!r} (count={html.count(old)})"
    html = html.replace(old, new)


def replace_var_line(name, code):
    global html
    i = html.index(f"var {name}")
    ls = html.rfind("\n", 0, i) + 1
    le = html.index("\n", i)
    html = html[:ls] + "  " + code + "\n" + html[le + 1:]


# ---------- header ----------
rep("<title>Boltz-01 Prediction</title>", f"<title>Boltz-02 Prediction</title>")
rep("<h1>boltz-01</h1>", f"<h1>{EXP}</h1>")
rep(
    "<span><b>chains</b> A (ligand) &middot; B (protein, 380 aa)</span>",
    f"<span><b>chains</b> A (ligand) &middot; B (protein, {aa_count} aa)</span>",
)
rep("<span><b>model output</b> boltz-01_model_0.cif</span>",
    f"<span><b>model output</b> {EXP}_model_0.cif</span>")

# ---------- KPI tiles ----------
rep('<span class="value">0.79</span>', f'<span class="value">{conf["confidence_score"]:.2f}</span>')
rep('<span class="value">0.73</span>', f'<span class="value">{conf["ptm"]:.2f}</span>')
rep('<span class="value">0.88</span>', f'<span class="value">{conf["iptm"]:.2f}</span>')
rep('<span class="value">76.8%</span>', f'<span class="value">{conf["complex_plddt"]*100:.1f}%</span>')
rep('<span class="value">80.1%</span>', f'<span class="value">{conf["complex_iplddt"]*100:.1f}%</span>')
rep('<span class="value">0.86</span>', f'<span class="value">{conf["complex_pde"]:.2f}</span>')
rep('<span class="value">3.32</span>', f'<span class="value">{conf["complex_ipde"]:.2f}</span>')

# ---------- composition ----------
rep(
    '<td>Ligand &middot; <span class="mono">SMILES CCO</span> (ethanol, 3 heavy atoms)</td>',
    f'<td>Ligand &middot; <span class="mono">SMILES {smiles}</span> (acetic acid, {ligand_n} heavy atoms)</td>',
)
rep('<td class="ptm-num">0.998</td>',
    f'<td class="ptm-num">{conf["chains_ptm"]["0"]:.3f}</td>')
rep('<td class="ptm-num">0.730</td>',
    f'<td class="ptm-num">{conf["chains_ptm"]["1"]:.3f}</td>')
rep("<dt>Input</dt><dd>boltz-01.yaml</dd>", f"<dt>Input</dt><dd>{EXP}.yaml</dd>")
rep(
    '<div class="cmd">boltz predict boltz-01.yaml --use_msa_server</div>',
    f'<div class="cmd">boltz predict {EXP}.yaml --use_msa_server --num_workers 0 --override</div>',
)
rep(
    f'<td>Protein &middot; 380 aa<span class="chain-seq"',
    f'<td>Protein &middot; {aa_count} aa<span class="chain-seq"',
)

# ---------- section notes ----------
rep("Rendered directly from boltz-01_model_0.cif.", f"Rendered directly from {EXP}_model_0.cif.")
rep(
    "383 tokens: 3 ligand atoms (A) followed by 380 protein residues (B).",
    f"{dim} tokens: {ligand_n} ligand atoms (A) followed by {aa_count} protein residues (B).",
)
rep('viewBox="0 0 383 383"', f'viewBox="0 0 {dim} {dim}"')
rep(
    "Rows/columns 1&ndash;3 are the ligand (chain A); 4&ndash;383 are the protein (chain B).",
    f"Rows/columns 1&ndash;{ligand_n} are the ligand (chain A); {ligand_n+1}&ndash;{dim} are the protein (chain B).",
)
rep("Output files (boltz_results_boltz-01/)", f"Output files (boltz_results_{EXP}/)")
rep('"chain B · protein · 380 aa"', f'"chain B · protein · {aa_count} aa"')
rep('"← ligand (3 atoms)"', f'"← ligand ({ligand_n} atoms)"')

# ---------- JS data variables ----------
replace_var_line("CIF", "var CIF = " + json.dumps(cif) + ";")
replace_var_line("PLDDT", "var PLDDT = " + json.dumps([round(float(v) * 100, 2) for v in plddt]) + ";")
replace_var_line("PAE_B64", f'var PAE_B64 = "{pae_b64}";')
replace_var_line("PAE_DIM", f"var PAE_DIM = {dim};")
replace_var_line("PAE_MAX", f"var PAE_MAX = {pae_cap};")
replace_var_line(
    "PROTEIN_SEQ",
    "var PROTEIN_SEQ = " + json.dumps(protein_seq) + f"; // {aa_count}-char 1-letter sequence, chain B",
)
replace_var_line("LIGAND_N", f"var LIGAND_N = {ligand_n};            // {ligand_n}")
replace_var_line("MANIFEST", "var MANIFEST = " + json.dumps(manifest) + ";")

with open(OUTPUT, "w") as f:
    f.write(html)

print(f"written: {OUTPUT}")
print(f"dim={dim} ligand_n={ligand_n} aa={aa_count}")
print(f"pae_max={pae_max:.4f} cap={pae_cap}")
print(f"conf={conf['confidence_score']:.3f} ptm={conf['ptm']:.3f} iptm={conf['iptm']:.3f}")
print(f"complex_plddt={conf['complex_plddt']*100:.1f}% complex_iplddt={conf['complex_iplddt']*100:.1f}%")
print(f"pde={conf['complex_pde']:.2f} ipde={conf['complex_ipde']:.2f}")
print(f"chains_ptm={conf['chains_ptm']}")
print(f"manifest entries={len(manifest)}")
