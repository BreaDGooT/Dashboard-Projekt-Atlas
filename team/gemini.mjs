#!/usr/bin/env node
// Gemini als Team-Mitglied: Claude Code (Dirigent) delegiert Recherche, Texte und Bilder.
//
//   ./team/gemini.sh models                      verfügbare Modelle anzeigen
//   ./team/gemini.sh text  "Prompt"              Text-Antwort (Flash, Free Tier)
//   ./team/gemini.sh image "Prompt" out.png      Bild erzeugen und speichern
//
// Schlüssel: bevorzugt als API-Credential der Cloud-Umgebung (Proxy setzt den Header x-goog-api-key,
// der Schlüssel ist in der Sitzung nie sichtbar). Alternativ Umgebungsvariable GEMINI_API_KEY.
// Modelle optional überschreiben: GEMINI_TEXT_MODEL, GEMINI_IMAGE_MODEL.

import { writeFile } from 'node:fs/promises';

const API = 'https://generativelanguage.googleapis.com/v1beta';
const KEY = process.env.GEMINI_API_KEY;

function fail(msg) {
  console.error(`Gemini: ${msg}`);
  process.exit(1);
}

async function call(path, body) {
  const headers = { 'content-type': 'application/json' };
  if (KEY) headers['x-goog-api-key'] = KEY; // sonst ergänzt der Proxy den Schlüssel (API-Credential)
  const res = await fetch(`${API}/${path}`, {
    method: body ? 'POST' : 'GET',
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const reason = data.error?.message || res.statusText;
    const msg = res.status === 429 ? `Limit erreicht (429): ${reason}`
      : !KEY && [400, 401, 403].includes(res.status) ? `Kein gültiger Schlüssel angekommen (${res.status}). API-Credential für generativelanguage.googleapis.com prüfen oder GEMINI_API_KEY setzen. Google meldet: ${reason}`
      : `Fehler ${res.status}: ${reason}`;
    throw Object.assign(new Error(msg), { status: res.status });
  }
  return data;
}

// Überlastet (503), abgeschaltet (404) oder Kontingent weg (429): nächstes Modell versuchen.
const RETRY = [404, 429, 500, 503];

async function generate(kind, body) {
  const models = await pickModels(kind);
  for (const [i, model] of models.slice(0, 3).entries()) {
    try {
      return { model, data: await call(`models/${model}:generateContent`, body) };
    } catch (e) {
      if (!RETRY.includes(e.status) || i === Math.min(models.length, 3) - 1) throw e;
      console.error(`[${model}] ${e.status} – weiter mit nächstem Modell`);
    }
  }
}

async function listModels() {
  const out = [];
  let pageToken = '';
  do {
    const data = await call(`models?pageSize=200${pageToken ? `&pageToken=${pageToken}` : ''}`);
    out.push(...(data.models || []));
    pageToken = data.nextPageToken || '';
  } while (pageToken);
  return out.filter(m => (m.supportedGenerationMethods || []).includes('generateContent'));
}

// Passende Modelle, neuestes zuerst, falls keins vorgegeben ist.
async function pickModels(kind) {
  const override = kind === 'image' ? process.env.GEMINI_IMAGE_MODEL : process.env.GEMINI_TEXT_MODEL;
  if (override) return [override];
  const names = (await listModels()).map(m => m.name.replace('models/', ''));
  const candidates = names.filter(n =>
    n.includes('flash') && !n.includes('lite') && !n.includes('tts') && !n.includes('live') &&
    (kind === 'image' ? n.includes('image') : !n.includes('image'))
  );
  if (!candidates.length) fail(`Kein passendes ${kind}-Modell gefunden. Mit "models" prüfen.`);
  const version = n => (n.match(/(\d+(?:\.\d+)?)/) || [0, 0])[1] * 1;
  candidates.sort((a, b) => version(b) - version(a) || a.includes('preview') - b.includes('preview'));
  return candidates;
}

const [cmd, prompt, outFile] = process.argv.slice(2);

try {
if (cmd === 'models') {
  for (const m of await listModels()) console.log(m.name.replace('models/', ''));
} else if (cmd === 'text' && prompt) {
  const { model, data } = await generate('text', { contents: [{ parts: [{ text: prompt }] }] });
  const text = (data.candidates?.[0]?.content?.parts || []).map(p => p.text || '').join('');
  console.error(`[${model}]`);
  console.log(text.trim());
} else if (cmd === 'image' && prompt && outFile) {
  const { model, data } = await generate('image', {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { responseModalities: ['TEXT', 'IMAGE'] },
  });
  const parts = data.candidates?.[0]?.content?.parts || [];
  const img = parts.find(p => p.inlineData?.data);
  if (!img) fail(`Kein Bild erhalten. Antwort: ${parts.map(p => p.text || '').join(' ').slice(0, 300)}`);
  await writeFile(outFile, Buffer.from(img.inlineData.data, 'base64'));
  console.error(`[${model}]`);
  console.log(`Bild gespeichert: ${outFile}`);
} else {
  console.log('Nutzung: gemini.sh models | text "Prompt" | image "Prompt" datei.png');
  process.exit(cmd ? 1 : 0);
}
} catch (e) {
  fail(e.message);
}
