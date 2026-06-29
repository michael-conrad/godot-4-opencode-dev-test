#!/usr/bin/env bash
# Rebuild all Ollama models from their modelfiles.
# Run from cards/modelfiles/ directory.
# Usage: bash rebuild-all.sh [model-name-prefix]
#   (optional prefix to rebuild only matching models)

set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# Mapping: modelfile → model name (tag format: <family>:<size>-<context>)
declare -A MODELS
MODELS[devstral-small2-384k.modelfile]="devstral-small-2:24b-384k"
MODELS[gemma4-31b-256k.modelfile]="gemma4:31b-256k"
MODELS[gpt-oss20b-128k.modelfile]="gpt-oss:20b-128k"
MODELS[granite4.1-30b-128k.modelfile]="granite4.1:30b-128k"
MODELS[laguna-xs.2-256k.modelfile]="laguna-xs.2:q4_K_M-256k"
MODELS[llama3.2-3b-128k.modelfile]="llama3.2:3b-128k"
MODELS[mistral-small3.2-32k.modelfile]="mistral-small3.2:24b-32k"
MODELS[nemotron-cascade30b-256k.modelfile]="nemotron-cascade-2:30b-256k"
MODELS[nemotron3-33b-256k.modelfile]="nemotron3:33b-256k"
MODELS[qwen3-coder-30b-256k.modelfile]="qwen3-coder:30b-256k"
MODELS[qwen3-embedding-40k.modelfile]="qwen3-embedding:40k"
MODELS[qwen3.5-35b-256k.modelfile]="qwen3.5:35b-256k"
MODELS[qwen3.6-35b-256k.modelfile]="qwen3.6:35b-256k"
MODELS[ornith-35b-256k.modelfile]="ornith:35b-256k"

PREFIX="${1:-}"

for modelfile in "${!MODELS[@]}"; do
    model="${MODELS[$modelfile]}"
    [[ -n "$PREFIX" && "$model" != "$PREFIX"* ]] && continue
    echo "=== $modelfile → $model ==="
    ollama create "$model" -f "$modelfile"
    echo ""
done

echo "Done."
