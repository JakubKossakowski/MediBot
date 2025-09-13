"use client";

import { useEffect, useState } from "react";
import { getSettings, putSettings, AgentSettings } from "@/lib/api";

const AVAILABLE_MODELS = [
  "gpt-4o-mini",
  "gpt-4o",
  "gpt-4.1",
  "claude-3.5-sonnet",
];

const AVAILABLE_VOICES = [
  "H5xTcsAIeS5RAykjz57a",
  "S1uaQ66tHSeCjgsWYpGI",
  "N0GCuK2B0qwWozQNTS8F",
  "d4Z5Fvjohw3zxGpV8XUV",
];

export default function SettingsPage() {
  const [settings, setSettings] = useState<AgentSettings | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    getSettings()
      .then((s) => {
        setSettings(s);
      })
      .catch((e) => setError(String(e)));
  }, []);

  const onSave = async () => {
    if (!settings) return;
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      const updated = await putSettings(settings);
      setSettings(updated);
      setSuccess("Ustawienia zapisane");
    } catch (e: any) {
      setError(e?.message ?? "Błąd zapisu");
    } finally {
      setSaving(false);
    }
  };

  if (!settings) return <div className="p-6">Ładowanie…</div>;

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Ustawienia AI Agenta</h1>

      <div className="grid grid-cols-1 gap-6">
        <div className="space-y-2">
          <label className="block text-sm font-medium">Model LLM</label>
          <select
            className="w-full rounded-xl border p-3"
            value={settings.llm_model}
            onChange={(e) => setSettings({ ...settings, llm_model: e.target.value })}
          >
            {AVAILABLE_MODELS.map((m) => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium">Głos TTS</label>
          <select
            className="w-full rounded-xl border p-3"
            value={settings.voice}
            onChange={(e) => setSettings({ ...settings, voice: e.target.value })}
          >
            {AVAILABLE_VOICES.map((v) => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium">Temperatura</label>
          <input
            type="range"
            min={0}
            max={1}
            step={0.1}
            value={settings.temperature}
            onChange={(e) => setSettings({ ...settings, temperature: Number(e.target.value) })}
            className="w-full"
          />
          <div className="text-sm text-gray-600">{settings.temperature.toFixed(1)}</div>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium">Język</label>
          <input
            className="w-full rounded-xl border p-3"
            value={settings.language}
            onChange={(e) => setSettings({ ...settings, language: e.target.value })}
          />
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium">Ton wypowiedzi</label>
          <select
            className="w-full rounded-xl border p-3"
            value={settings.tone}
            onChange={(e) => setSettings({ ...settings, tone: e.target.value })}
          >
            {["friendly", "formal", "concise", "empathetic"].map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={onSave}
          disabled={saving}
          className="rounded-2xl px-5 py-3 bg-black text-white disabled:opacity-50 shadow-md"
        >
          {saving ? "Zapisywanie…" : "Zapisz ustawienia"}
        </button>
        {success && <span className="text-green-600 text-sm">{success}</span>}
        {error && <span className="text-red-600 text-sm">{error}</span>}
      </div>
    </div>
  );
}
