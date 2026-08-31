# Boltz Guide

Setup and usage notes for running [Boltz](https://github.com/jwohlwend/boltz) structure and binding predictions locally on a GPU pod.

## Prerequisites

- A Linux pod/VM with an NVIDIA GPU and CUDA drivers installed
- `sudo` access to install system packages
- `python3.12`

## Installation

### 1. Install system dependencies

```bash
sudo apt update
sudo apt install -y python3.12-dev build-essential
```

### 2. (Optional) Install Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### 3. Clone this repository

```bash
git clone https://github.com/drai-inn/boltz-guide.git
cd boltz-guide
git checkout test
```

### 4. Create a virtual environment and install Boltz

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U boltz[cuda]
```

## Usage

### 1. Define an input sequence

Create a YAML file describing the entities to predict (see [`boltz-01.yaml`](boltz-01.yaml) for a minimal ligand–protein binding example):

```yaml
sequences:
  - ligand:
      id: A
      smiles: "CCO"

  - protein:
      id: B
      sequence: EGAGGANDKKKISSERRKEKSRDAARSRRSKESEVFYELAHQLPLPHNVSSHLDKASVMRLTISYLRVRKLLDAGDLDIEDDMKAQMNCFYLKALDGFVMVLTDDGDMIYISDNVNKYMGLTQFELTGHSVFDFTHPCDHEEMREMLTHRNGLVKKGKEQNTQRSFFLRMKCTLTSRGRTMNIKSATWKVLHCTGHIHVYDTNSNQPQCGYKKPPMTCLVLICEPIPHPSNIEIPLDSKTFLSRHSLDMKFSYCDERITELMGYEPEELLGRSIYEYYHALDSDHLTKTHHDMFTKGQVTTGQYRMLAKRGGYVWVETQATVIYNTKNSQPQCIVCVNYVVSGIIQHDLIFSLQQTECVLKPVESSDMKMTQLFTKVESE

binding:
  type: ligand_protein
  binder: A
  target: B

num_samples: 1
```

### 2. Run a prediction

```bash
boltz predict boltz-01.yaml --use_msa_server
```

To re-run and overwrite existing results without using multiprocessing workers:

```bash
boltz predict boltz-01.yaml --use_msa_server --num_workers 0 --override
```

Results are written to a `boltz_results_<input-name>/` directory alongside the input YAML.

### 3. Visualize the results

This repo is set up to work with [Claude Code](https://claude.com/claude-code). Once a prediction has finished, just ask Claude to look at the output, e.g.:

> Visualize the results in `boltz_results_boltz-01`

Claude will read the predicted structure and confidence scores and build an interactive HTML report — a 3D structure viewer (colored by pLDDT confidence and by chain), a per-residue confidence chart, and a predicted aligned error (PAE) heatmap. It publishes the report as a shareable link and also saves a copy as `report.html` inside that run's `boltz_results_<input-name>/` folder, so the visualization stays with the experiment (see [`CLAUDE.md`](CLAUDE.md)).

## Repository Layout

| Path | Description |
|---|---|
| `boltz-01.yaml` | Example input sequence for a local `boltz predict` run |
| `boltz-experiments/` | Output artifacts from prediction runs |
| `boltz_results_<name>/` | Output of a `boltz predict` run; `report.html` inside it is the visualization described above |
| `CLAUDE.md` | Project rules for Claude Code, incl. where visualization reports get saved |

## References

- Upstream project: [jwohlwend/boltz](https://github.com/jwohlwend/boltz)
