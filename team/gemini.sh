#!/usr/bin/env bash
# Startet den Gemini-Mitarbeiter. NODE_USE_ENV_PROXY lässt Nodes fetch den Proxy der Umgebung nutzen.
set -euo pipefail
NODE_USE_ENV_PROXY=1 exec node --no-warnings "$(dirname "$0")/gemini.mjs" "$@"
