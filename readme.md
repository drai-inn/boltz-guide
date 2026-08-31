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

## Repository Layout

| Path | Description |
|---|---|
| `boltz-01.yaml` | Example input sequence for a local `boltz predict` run |
| `boltz-experiments/` | Output artifacts from prediction runs |

## References

- Upstream project: [jwohlwend/boltz](https://github.com/jwohlwend/boltz)
