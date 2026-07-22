# Boltz Guide

**Goal:** Give researchers access to both the **Boltz API** and **DRAI's LLM models** (via the OpenCode harness) for drug discovery work.

---

## 1. Setup

### Prerequisite
- A local Linux system (or equivalent console) where you can install software.

### 1a. OpenCode

1. **Install** using the official installer:
   ```bash
   curl -fsSL https://opencode.ai/install | bash
   ```

2. **Add the binary to your PATH** by appending this line to `~/.bashrc`, then reload:
   ```bash
   echo 'export PATH="$HOME/.opencode/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Test** that it runs:
   ```bash
   opencode
   ```
   Confirm it launches, then exit.

4. **Configure DRAI access.** Create `~/.config/opencode/opencode.json` with exactly the following. This points OpenCode at our DRAI-hosted DGX Spark box and lists the available models (Qwen3.6 in this example):
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

### 1b. Boltz

1. **Install** the `boltz-api` CLI:
   ```bash
   curl -fsSL https://install.boltz.bio/boltz-api/install.sh | sh
   ```

2. **PATH** — the installer places `boltz-api` in `~/.local/bin`, which is already on your PATH from the OpenCode step. No further action needed. (If `boltz-api` isn't found, run `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc`.)

3. **Log in:**
   ```bash
   boltz-api auth login
   ```
   If you don't have an account yet, create a trial account using your **UoA Google login**.

4. **Create your working folder** and add the instruction file:
   ```bash
   mkdir -p ~/boltz-experiments
   ```
   Create `~/boltz-experiments/boltz-instructions.txt` with the following content. **This is a starting template — feel free to update it to suit your own experiments.**
   ```
   I want to use the Boltz API to predict structure and binding. Please follow this exact pattern:

   Create the input YAML payload in the current directory and pass it via @yaml://./<filename>.yaml.

   Run boltz-api predictions:structure-and-binding estimate-cost --model boltz-2.1 --input @yaml://./<filename>.yaml and ask me for confirmation before proceeding.

   Submit the job using an idempotency key and print the ID cleanly using:
   boltz-api predictions:structure-and-binding start --model boltz-2.1 --idempotency-key "<run-name>" --input @yaml://./<filename>.yaml --raw-output --transform id

   Download the results into my boltz-experiments folder using:
   boltz-api download-results --id "<job-id>" --name "<run-name>" --root-dir "~/boltz-experiments" --poll-interval-seconds 10

   Keep all boltz-api calls as top-level commands (do not use backgrounding like & or nohup).
   ```

### 1c. Connect OpenCode to DRAI

1. Go to your working folder and launch OpenCode:
   ```bash
   cd ~/boltz-experiments
   opencode
   ```
2. Type `/connect` to connect to DRAI's API. A list of providers appears.
3. Start typing `DRAI` — it will surface **DRAI UoA models**. Select it.
4. Enter the API key provided to you by **Chris or Jun**, then press Enter.
5. You now have access to **Qwen3.6-35B-A3B** by default — you should see it just below the chat prompt window. If not, type `/model` and select **Qwen3.6-35B-A3B** under **DRAI UoA models**.

---

## 2. Running the Experiment (OpenCode + Boltz)

1. If you're not already in OpenCode, launch it from your working folder:
   ```bash
   cd ~/boltz-experiments
   opencode
   ```
2. Prompt it to note that there's an instruction `.txt` file in the current folder, and ask it to do a **quick smoke test**. For example:
   > There's an instruction txt file in the current folder. Please read it and run a quick smoke test.
3. **Note (Not relevant to Qwen model):** the Gemma model tends to work in small steps and may pause mid-task waiting for explicit permission. If it stops, simply follow up with `please continue`.
