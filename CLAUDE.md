# Project Atlas – Regeln für Claude Code

- Sprache: Deutsch. Flo mit „du“ ansprechen.
- **Nie** Yoummday- oder Telekom-Inhalte einbeziehen (Projekte, Aufgaben, Texte, Daten).
- Datenquelle: Notion „Flo Dashboard“ – nur die Datenbanken Projekte, Aufgaben, Meilensteine. Belege & Abos, Fristen-Tresor, Haustiere, Anbieter-Zuordnung und Ideen-Backlog nicht anbinden.
- Hub-Seite mit Plan, Entscheidungen und offenen Fragen: Notion „Project Atlas – Interaktives Projekt-Dashboard“. Entscheidungen dort im Entscheidungslog festhalten.
- KI-Status in der Notion-Datenbank „KI-Agenten“ pflegen, wenn Aufgaben an Gemini oder ChatGPT delegiert werden (siehe `team/README.md`).
- Das Dashboard zeigt diesen Status live („Echter Stand“). Deshalb bei Arbeitsbeginn und -ende für Claude Code und jede beauftragte KI setzen: `Status` (Arbeitet/Bereit/Offline), `Arbeitet an` (Projekt) und `Aktuelle Tätigkeit` (kurz, ohne Yoummday/Telekom).
- Aufgaben-Felder `Heute` (Tagesziel) und `Erledigt am` (Wochenrückblick) nicht umbenennen; `Erledigt am` beim Abhaken mitsetzen.
- Aufgaben mit `Zuständige KI` = ChatGPT oder Gemini: Wenn Flo eine Sitzung startet, erledigt Claude Code sie über `team/chatgpt.sh` bzw. `team/gemini.sh`, setzt dabei die Aufgabe auf „In Bearbeitung“ und den KI-Status, und am Ende Ergebnis in die Aufgabenseite, Status „Erledigt“ mit `Erledigt am`.
- Projekte-Feld `Bauplatz` (Bauplatz 1–3) setzt ein Projekt als Baustelle ins Dorf; nicht umbenennen.
- Keine Kennzahlen, Stände oder Termine erfinden; Demo-Daten immer als solche kennzeichnen.
- Prototyp: `prototype/index.html` (eine Datei, kein Build).
