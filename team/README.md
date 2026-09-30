# KI-Team

Claude Code ist der **Dirigent**: Er nimmt Flos Auftrag an, verteilt Teilaufgaben an die anderen KIs, führt die Ergebnisse zusammen und trägt den Status in Notion ein (Datenbank „KI-Agenten“). Das Dashboard zeigt so immer, wer woran arbeitet – ohne manuelles Klicken.

| Mitglied | Rolle | Anbindung | Stand |
|---|---|---|---|
| Claude Code | Dirigent, Code, Zusammenführung | läuft hier | aktiv |
| Gemini | Recherche, Texte, Bilder | `team/gemini.sh` über API-Schlüssel `GEMINI_API_KEY` | bereit, wartet auf Schlüssel |
| ChatGPT | Zweitmeinung, Bilder, Codex-Aufgaben | Codex CLI (ChatGPT-Plus-Login) oder OpenAI-API | geplant – Netzwerkfreigabe für `api.openai.com` und `auth.openai.com` nötig |
| Claude (App) | Konzept & Texte im Chat mit Flo | Notion-Konnektor | manuell / One-Klick |

## Gemini einrichten (einmalig)

1. In Google AI Studio einen API-Schlüssel erstellen (Google-Konto, keine Kreditkarte nötig).
2. In den Einstellungen der Cloud-Umgebung als Umgebungsvariable `GEMINI_API_KEY` hinterlegen – nie im Chat einfügen.
3. Neue Sitzung starten; dann `./team/gemini.sh models` zum Test.

## Nutzung

```bash
./team/gemini.sh text  "Recherchiere …"
./team/gemini.sh image "Pixel-Art Dorf …" assets/karte.png
```

## Regeln

- Nur Claude Code schreibt Code und committet.
- Keine Yoummday-/Telekom-Inhalte an irgendein Team-Mitglied.
- Schlüssel nur als Umgebungsvariable, nie im Repo.
- Kosten: Text über Gemini Flash im Free Tier; Bilder können je nach Modell und Tarif pro Bild kosten – vor größeren Bild-Serien Kosten prüfen.
