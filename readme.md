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

## Running via OpenCode + DRAI local model

Instead of running `boltz predict` directly, you can drive the **Boltz API**
through [OpenCode](https://opencode.ai) wired up to DRAI's locally-hosted
LLM (Qwen3.6-35B-A3B). This lets an agent handle YAML creation, cost
estimation, job submission, and result download for you. Full details:
[drai-inn/boltz-guide: BOLTZ_GUIDE.md](https://github.com/drai-inn/boltz-guide/blob/master/BOLTZ_GUIDE.md).

### 1. Install and configure OpenCode

```bash
curl -fsSL https://opencode.ai/install | bash
echo 'export PATH="$HOME/.opencode/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
opencode   # confirm it launches, then exit
```

Point OpenCode at DRAI's DGX Spark box by creating
`~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "litellm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "DRAI UoA models",
      "options": {
        "baseURL": "https://litellm.test.drai.auckland.ac.nz/v1"
      },
      "models": {
        "Qwen3.6-35B-A3B": {
          "name": "Qwen3.6-35B-A3B"
        }
      }
    }
  }
}
```

### 2. Install the `boltz-api` CLI

```bash
curl -fsSL https://install.boltz.bio/boltz-api/install.sh | sh
boltz-api auth login   # trial accounts can sign in with a UoA Google login
```

### 3. Set up a working folder and instructions file

```bash
mkdir -p ~/boltz-experiments
```

Create `~/boltz-experiments/boltz-instructions.txt` telling the agent the
exact command pattern to follow — build the YAML payload, estimate cost and
confirm before submitting, submit with an idempotency key, then download the
results. See the upstream guide for the template text; keep all `boltz-api`
calls as top-level commands (no `&`/`nohup` backgrounding).

### 4. Connect OpenCode to DRAI and run

```bash
cd ~/boltz-experiments
opencode
```

Inside OpenCode: type `/connect`, search for **DRAI UoA models**, select it,
and enter the API key provided by Chris or Jun. Confirm **Qwen3.6-35B-A3B**
is selected (`/model` if not), then prompt it to read the instructions file
in the current folder and run a smoke test, e.g.:

> There's an instruction txt file in the current folder. Please read it and
> run a quick smoke test.

If the model pauses mid-task waiting for permission, just reply
`please continue`.

## Repository Layout

| Path | Description |
|---|---|
| `boltz-01.yaml` | Example input sequence for a local `boltz predict` run |
| `boltz_results_<name>/` | Output of a `boltz predict` run; `report.html` inside it is the visualization described above |
| `CLAUDE.md` | Project rules for Claude Code, incl. where visualization reports get saved |

## References

- Upstream project: [jwohlwend/boltz](https://github.com/jwohlwend/boltz)
