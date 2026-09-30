#!/usr/bin/env bash
# Startet den ChatGPT-Mitarbeiter über die Codex CLI mit Flos ChatGPT-Plus-Login.
# Der Login gilt pro Sitzung (Container): zuerst ./team/chatgpt.sh login
set -euo pipefail
export NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1
codex() { npx -y @openai/codex "$@"; }
IMG_DIR="$HOME/.codex/generated_images"

case "${1:-}" in
  login)  codex login --device-auth ;;
  status) codex login status ;;
  text)
    [ $# -ge 2 ] || { echo "Nutzung: $0 text \"Auftrag\"" >&2; exit 1; }
    codex exec --skip-git-repo-check --sandbox read-only "$2"
    ;;
  image)
    [ $# -ge 3 ] || { echo "Nutzung: $0 image \"Beschreibung\" ziel.png [vorlage.png]" >&2; exit 1; }
    marker=$(mktemp); trap 'rm -f "$marker"' EXIT
    ref=(); [ -n "${4:-}" ] && ref=(-i "$4")   # optionale Vorlage, z. B. Kartenausschnitt für einheitlichen Stil
    codex exec --skip-git-repo-check --sandbox read-only \
      "Erzeuge mit deinem eingebauten Bildwerkzeug genau ein Bild: $2. Antworte danach nur mit OK." ${ref[@]+"${ref[@]}"} >&2
    # Codex legt Bilder unter ~/.codex/generated_images ab; das neueste seit dem Start übernehmen.
    img=$(find "$IMG_DIR" -type f -name '*.png' -newer "$marker" -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
    [ -n "$img" ] || { echo "Kein Bild erzeugt – Bildwerkzeug fehlt oder Limit erreicht (siehe Ausgabe oben)." >&2; exit 1; }
    mkdir -p "$(dirname "$3")"
    cp "$img" "$3"
    echo "$3"
    ;;
  *)
    echo "Nutzung: $0 login | status | text \"Auftrag\" | image \"Beschreibung\" ziel.png [vorlage.png]" >&2
    exit 1
    ;;
esac
