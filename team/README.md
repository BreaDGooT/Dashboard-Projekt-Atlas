# KI-Team

Claude Code ist der **Dirigent**: Er nimmt Flos Auftrag an, verteilt Teilaufgaben an die anderen KIs, führt die Ergebnisse zusammen und trägt den Status in Notion ein (Datenbank „KI-Agenten“). Das Dashboard zeigt so immer, wer woran arbeitet – ohne manuelles Klicken.

| Mitglied | Rolle | Anbindung | Stand |
|---|---|---|---|
| Claude Code | Dirigent, Code, Zusammenführung | läuft hier | aktiv |
| Gemini | Recherche, Texte (Bilder erst mit Abrechnung) | `team/gemini.sh` – Schlüssel als API-Credential (oder `GEMINI_API_KEY`) | aktiv für Text (getestet 30.09.2026) |
| ChatGPT | Zweitmeinung, Bilder, Codex-Aufgaben | Codex CLI (ChatGPT-Plus-Login) oder OpenAI-API | geplant – Netzwerkfreigabe für `api.openai.com` und `auth.openai.com` nötig |
| Claude (App) | Konzept & Texte im Chat mit Flo | Notion-Konnektor | manuell / One-Klick |

## Gemini einrichten (einmalig)

1. In Google AI Studio einen API-Schlüssel erstellen (Google-Konto, keine Kreditkarte nötig).
2. Auf claude.ai/code im Browser: Cloud-Symbol mit dem Umgebungsnamen über dem Eingabefeld → beim Eintrag auf das Zahnrad → **Update cloud environment**.
3. Empfohlen – **API credentials** → **Add credential**: Name `Gemini API`, Allowed websites `generativelanguage.googleapis.com`, Custom header Name `x-goog-api-key`, Prefix leeren, Value = Schlüssel → **Connect**. Der Schlüssel ist danach in keiner Sitzung sichtbar.
   Alternative: unter **Environment variables** die Zeile `GEMINI_API_KEY=…` eintragen → **Save changes**.
4. Neue Sitzung starten; dann `./team/gemini.sh models` zum Test.

## Nutzung

```bash
./team/gemini.sh text  "Recherchiere …"
./team/gemini.sh image "Pixel-Art Dorf …" assets/karte.png
```

Das Skript nimmt das neueste passende Flash-Modell. Ist es überlastet (503), abgeschaltet (404) oder das Kontingent erschöpft (429), versucht es automatisch die nächsten zwei.

## Teststand (30.09.2026)

- Schlüssel kommt über das API-Credential an, Modellliste abrufbar.
- **Text:** funktioniert im Free Tier. `gemini-3.8-flash` und `gemini-3.7-flash` meldeten beim Test 503 (Überlast), `gemini-3.6-flash` antwortete.
- **Bilder:** im Free Tier gesperrt (Google meldet Limit 0 für alle Bildmodelle). Erst nutzbar, wenn im Google-AI-Studio-Projekt die Abrechnung aktiviert ist.

## Regeln

- Nur Claude Code schreibt Code und committet.
- Keine Yoummday-/Telekom-Inhalte an irgendein Team-Mitglied.
- Schlüssel nur als Umgebungsvariable, nie im Repo.
- Kosten: Text über Gemini Flash im Free Tier; Bilder können je nach Modell und Tarif pro Bild kosten – vor größeren Bild-Serien Kosten prüfen.
