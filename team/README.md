# KI-Team

Claude Code ist der **Dirigent**: Er nimmt Flos Auftrag an, verteilt Teilaufgaben an die anderen KIs, führt die Ergebnisse zusammen und trägt den Status in Notion ein (Datenbank „KI-Agenten“). Das Dashboard zeigt so immer, wer woran arbeitet – ohne manuelles Klicken.

| Mitglied | Rolle | Anbindung | Stand |
|---|---|---|---|
| Claude Code | Dirigent, Code, Zusammenführung | läuft hier | aktiv |
| Gemini | Recherche, Texte (Bilder erst mit Abrechnung) | `team/gemini.sh` – Schlüssel als API-Credential (oder `GEMINI_API_KEY`) | aktiv für Text (getestet 30.09.2026) |
| ChatGPT | Bilder, Zweitmeinung | `team/chatgpt.sh` – Codex CLI mit ChatGPT-Plus-Login (Gerätecode, pro Sitzung) | aktiv für Bilder und Text (getestet 30.09.2026) |
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
./team/gemini.sh image "Pixel-Art Dorf …" assets/karte.png   # erst mit Google-Abrechnung

./team/chatgpt.sh status                                       # Login noch gültig?
./team/chatgpt.sh image "Pixel-Art Dorfhaus …" assets/haus.png
./team/chatgpt.sh image "Nahansicht des Gebäudes …" assets/haus.png vorlage.png [stil.png …]   # eine oder mehrere Bildvorlagen
./team/chatgpt.sh text  "Zweitmeinung zu …"
```

Das Skript nimmt das neueste passende Flash-Modell. Ist es überlastet (503), abgeschaltet (404) oder das Kontingent erschöpft (429), versucht es automatisch die nächsten zwei.

## Teststand (30.09.2026)

- Schlüssel kommt über das API-Credential an, Modellliste abrufbar.
- **Text:** funktioniert im Free Tier. `gemini-3.8-flash` und `gemini-3.7-flash` meldeten beim Test 503 (Überlast), `gemini-3.6-flash` antwortete.
- **Bilder:** im Free Tier gesperrt (Google meldet Limit 0 für alle Bildmodelle). Erst nutzbar, wenn im Google-AI-Studio-Projekt die Abrechnung aktiviert ist.
- **ChatGPT (Codex 0.159.2):** Login per Gerätecode klappt über den Proxy der Umgebung. Bilder kommen über das eingebaute Bildwerkzeug (1254 × 1254 px PNG, ohne API-Schlüssel), Text über `codex exec`. Mit Bildvorlage (`-i`) übernimmt ChatGPT Form, Farben und Details zuverlässig (Stiltest Gebäude-Illustrationen). Der Proxy blockiert dabei `ab.chatgpt.com` und `*.oaiusercontent.com` – das sind Nebendienste, Bilder kommen trotzdem an. Gegenprüfung Gemini am selben Tag: `gemini-3.8-flash` und `gemini-3.7-flash` weiter 503, `gemini-3.6-flash` antwortet.

## ChatGPT einrichten (Bilder über das Plus-Abo)

Die Bildgenerierung in Codex (`image_generation`, in Codex 0.159 stabil) läuft über den ChatGPT-Login und zählt gegen die Codex-Limits des Abos. Es gibt keine Abrechnung pro Bild wie bei der API.

1. Auf claude.ai/code: Cloud-Umgebung → Zahnrad → **Update cloud environment** → **Network access**: `auth.openai.com`, `chatgpt.com` und `api.openai.com` erlauben.
2. Neue Sitzung starten. Claude Code führt `./team/chatgpt.sh login` aus und zeigt einen Link mit Code (15 Minuten gültig).
3. Flo öffnet den Link, meldet sich mit dem ChatGPT-Konto an und gibt den Code ein. Falls ChatGPT das verlangt, vorher unter Einstellungen → Sicherheit die Gerätecode-Anmeldung für Codex erlauben.
4. Der Login gilt für diese Sitzung (Container), in jeder neuen Sitzung ist er noch einmal nötig.

Laut einem offenen Codex-Fehlerbericht (openai/codex#37496) fehlt bei manchen Konten trotz Login das Bildwerkzeug. Flos Konto ist nicht betroffen (Test 30.09.2026). Alternative wäre die OpenAI-API mit eigenem Schlüssel, die aber pro Bild kostet.

## Regeln

- Nur Claude Code schreibt Code und committet.
- Keine Yoummday-/Telekom-Inhalte an irgendein Team-Mitglied.
- Schlüssel nur als Umgebungsvariable, nie im Repo.
- Kosten: Text über Gemini Flash im Free Tier; Bilder können je nach Modell und Tarif pro Bild kosten – vor größeren Bild-Serien Kosten prüfen.
