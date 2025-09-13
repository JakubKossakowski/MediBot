// src/lib/api.ts
const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "";

export type AgentSettings = {
  llm_model: string;
  voice: string;
  temperature: number;
  language: string;
  tone: string;
};

export async function getSettings(): Promise<AgentSettings> {
  const res = await fetch(`${BASE}/api/settings`, { cache: "no-store" });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to fetch settings: ${res.status} ${text}`);
  }
  return res.json();
}

export async function putSettings(payload: AgentSettings): Promise<AgentSettings> {
  const res = await fetch(`${BASE}/api/settings`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Failed to save settings: ${res.status} ${text}`);
  }
  return res.json();
}
