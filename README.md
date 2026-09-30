# Project Atlas

Interaktives, animiertes Projekt-Dashboard für Flos eigene Projekte – eine Pixelwelt, in der jedes Projekt ein Gebäude ist und KI-Agenten (Claude, Claude Code, ChatGPT, Gemini) sichtbar zu den Projekten laufen, an denen sie arbeiten.

## Stand

- **Phase 0 – Stil:** Hybrid entschieden (Pixelwelt + moderne Glas-Panels).
- **Prototyp v0.2:** [`prototype/index.html`](prototype/index.html) – ohne Build-Schritt; die Welt basiert auf einer von ChatGPT gemalten Dorf-Karte (`prototype/assets/dorf.webp`), darüber liegt die Animationsebene (Wasser, Licht, Figuren, Tiere, Wind, Tag/Nacht, Zoom).
  - Neue Karte? In `prototype/` ausführen: `python3 tools/build_mapdata.py` (erzeugt Lichter-Ebene und Wasser-Daten).
  - Projekte, Aufgaben und Meilensteine sind ein Snapshot aus Notion („Flo Dashboard“, Stand 30.09.2026).
  - KI-Aktivität: Umschalter zwischen **Demo** (simuliert) und **Echter Stand**.
  - Tageszeit der Welt folgt der Uhrzeit in Zypern (umschaltbar: Auto / Tag / Nacht).

## Datenquelle

Notion „Flo Dashboard“ – ausschließlich die Datenbanken **Projekte**, **Aufgaben** und **Meilensteine**.
Planung, Entscheidungen und offene Fragen stehen auf der Notion-Seite „Project Atlas – Interaktives Projekt-Dashboard“.

## Feste Regeln

- Yoummday / Telekom wird nie einbezogen.
- Nur Claude Code schreibt Code in dieses Repo; andere KIs liefern Texte, Bilder und Reviews zu.
- Oberfläche auf Deutsch.

## Nächste Phasen

1. **MVP:** echte Notion-Anbindung (live statt Snapshot), Login, Hosting.
2. **Live-Status:** Claude Code meldet sich per Hook automatisch; Echtzeit über Supabase.
3. **Vernetzung:** Status-Meldungen von Claude, ChatGPT und Gemini.
4. **Feinschliff:** Wetter, Sounds, Belohnungseffekte.
