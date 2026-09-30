# Project Atlas

Interaktives, animiertes Projekt-Dashboard für Flos eigene Projekte: eine Pixelwelt, in der jedes Projekt ein Gebäude ist und die KI-Agenten (Claude, Claude Code, ChatGPT, Gemini) sichtbar zu den Projekten laufen, an denen sie arbeiten. Notion bleibt die einzige Datenquelle; das Dashboard liest und schreibt direkt dorthin.

## Stand v1.0 (30.09.2026)

- **Prototyp:** [`prototype/index.html`](prototype/index.html), eine Datei ohne Build-Schritt. Die Welt basiert auf einer von ChatGPT gemalten Dorf-Karte (`prototype/assets/dorf.webp`), darüber liegt die Animationsebene (Wasser, Licht, Figuren, Tiere, Wetter, Tag/Nacht, Zoom).
- **Veröffentlicht** als privates Claude-Artifact (an Flos Seitenleiste angepinnt). Nur dort hat es die Notion-Verbindung.
- **Live aus Notion:** Projekte, Aufgaben, Meilensteine und KI-Agenten, Abgleich alle 2 Minuten. Änderungen im Dashboard landen sofort in Notion.

## Bedienung

| Bereich | Was geht |
|---|---|
| Dorf | Klick auf ein Gebäude zoomt hinein: Innenraum mit arbeitenden KIs links, alle Infos rechts. Freie Bauplätze („+“) legen ein neues Projekt an. |
| Detailansicht | Projektstatus, Fortschritt, Beschreibung; Aufgaben und Meilensteine anlegen, umbenennen (Klick auf den Titel), abhaken, Priorität, zuständige KI, Fälligkeit, für „Heute“ vormerken, entfernen. |
| Heute | Bis zu drei Aufgaben als Tagesziel. Vorschläge bevorzugen überfällige und heute fällige Aufgaben. |
| Fälligkeit | Kalender-Symbol an jeder offenen Aufgabe. Überfällig = rot, heute = gelb gefüllt, in 1–2 Tagen = gelb umrandet. Leeres Datum entfernt die Fälligkeit. |
| Projekt abschließen | Projektstatus „Erledigt“: Feuerwerk, danach Wimpelketten, Fahne und Funkeln am Gebäude. Baustellen lassen sich dann über „Bauplatz freigeben“ aus dem Dorf nehmen (das Projekt bleibt in Notion). |
| Menü | Projekte, Aufgaben (Filter nach Status, Projekt, Priorität, Fälligkeit, Heute), Rückblick (Kalenderwoche, erledigt, fällig, Meilensteine), KI-Agenten, Automationen, Notion-Sync, Einstellungen. |
| Wetter | Live über AccuWeather (Ort wählbar) oder Zufall nach Zypern-Klima; manuell umschaltbar. |

### Tastenkürzel

| Taste | Aktion |
|---|---|
| `/` | Suchen (im Dorf; im Aufgaben-Menü in der Aufgabenliste) |
| `P` / `A` / `R` / `K` / `N` / `E` | Projekte / Aufgaben / Rückblick / KI-Agenten / Notion-Sync / Einstellungen |
| `Esc` | Offene Ansicht schließen |
| `?` | Übersicht der Tastenkürzel |

Die Kürzel greifen nicht, solange ein Eingabefeld aktiv ist.

## Datenquelle Notion

Notion „Flo Dashboard“, ausschließlich die Datenbanken **Projekte**, **Aufgaben** und **Meilensteine**, dazu „KI-Agenten“ unter der Hub-Seite „Project Atlas – Interaktives Projekt-Dashboard“ (Plan, Entscheidungslog, offene Fragen).

Felder, die das Dashboard nutzt (nicht umbenennen):

| Datenbank | Feld | Zweck |
|---|---|---|
| Projekte | `Projektname`, `Status`, `Beschreibung`, `Fortschritt Prozent`, `Bereich` | Anzeige und Bearbeitung |
| Projekte | `Bauplatz` (Bauplatz 1–3) | setzt ein Projekt als Baustelle ins Dorf; leer = nicht im Dorf |
| Aufgaben | `Titel`, `Status`, `Priorität`, `Projekt` | Anzeige und Bearbeitung |
| Aufgaben | `Zuständige KI` | Figur läuft im „Echten Stand“ zu Aufgaben „In Bearbeitung“ |
| Aufgaben | `Heute` | Tagesziel |
| Aufgaben | `Erledigt am` | Wochenrückblick; wird beim Abhaken gesetzt |
| Aufgaben | `Fällig am` | Fälligkeit, Überfällig-Markierung, Vorschläge für „Heute“ |
| Meilensteine | `Titel`, `Status`, `Zieldatum`, `Projekt` | Anzeige, Feuerwerk beim Erreichen |
| KI-Agenten | `Status`, `Arbeitet an`, `Aktuelle Tätigkeit`, `Rolle im Projekt` | Echter KI-Stand im Dorf |

„Entfernen“ verschiebt Einträge in die Notion-Seite „Papierkorb (aus dem Dashboard entfernt)“. Endgültig löschen geht nur in Notion.

## KI-Team

Claude Code ist der Dirigent und verteilt Teilaufgaben an ChatGPT (`team/chatgpt.sh`) und Gemini (`team/gemini.sh`). Details und Einrichtung: [`team/README.md`](team/README.md).

So weiß das Dashboard, welche KI arbeitet:

1. Aufgabe in Notion oder im Dashboard anlegen und `Zuständige KI` setzen.
2. Startet Flo eine Claude-Code-Sitzung, erledigt Claude Code offene Aufgaben mit `Zuständige KI` = ChatGPT oder Gemini über das jeweilige Skript.
3. Dabei: Aufgabe auf „In Bearbeitung“, KI-Agenten-Eintrag auf „Arbeitet“ mit `Arbeitet an` und `Aktuelle Tätigkeit`.
4. Am Ende: Ergebnis in die Aufgabenseite, Status „Erledigt“ mit `Erledigt am`, KI wieder auf „Bereit“.

## Lokal starten

```bash
cd prototype
python3 -m http.server 8765
# dann http://127.0.0.1:8765/index.html öffnen
```

Außerhalb von Claude hat die Seite keine Notion-Verbindung. Sie zeigt dann den Offline-Stand vom 30.09.2026 und kann nichts speichern. Bearbeiten geht nur im veröffentlichten Artifact.

Neue Karte? In `prototype/` ausführen: `python3 tools/build_mapdata.py` (erzeugt Lichter-Ebene und Wasser-Daten).

## Umzug auf lokales Arbeiten (Vorbereitung)

Wenn Flo lokal mit der Claude-App (Claude Code) weitermachen will:

1. Repo klonen: `git clone https://github.com/BreaDGooT/Dashboard-Projekt-Atlas.git` und in der Claude-App als Projektordner öffnen. `CLAUDE.md` mit den Projektregeln wird automatisch geladen.
2. Notion-Konnektor in der Claude-App verbinden (derselbe Workspace „Flo Dashboard“).
3. ChatGPT: Node.js installieren, dann `./team/chatgpt.sh login` (die Skripte sind Bash: auf macOS/Linux direkt, unter Windows über WSL oder Git Bash). Lokal bleibt der Login bestehen, er muss nicht in jeder Sitzung neu erfolgen.
4. Gemini: Schlüssel als Umgebungsvariable `GEMINI_API_KEY` setzen (nie ins Repo).
5. Das Artifact bleibt unter derselben Adresse; Änderungen an `prototype/index.html` werden wie bisher daraus veröffentlicht.

## Ordner

| Pfad | Inhalt |
|---|---|
| `prototype/index.html` | das komplette Dashboard (HTML, CSS, JavaScript) |
| `prototype/assets/` | Dorf-Karte, Lichter, Haus-Illustrationen (`haeuser/`), Innenräume (`innen/`) |
| `prototype/tools/` | Hilfsskripte für die Kartendaten |
| `team/` | Skripte und Anleitung für ChatGPT und Gemini |
| `CLAUDE.md` | Regeln für Claude Code |

## Feste Regeln

- Yoummday / Telekom wird nie einbezogen.
- Nur Claude Code schreibt Code in dieses Repo; andere KIs liefern Texte, Bilder und Reviews zu.
- Keine erfundenen Kennzahlen, Stände oder Termine; Demo-Daten sind als solche gekennzeichnet.
- Oberfläche auf Deutsch.
