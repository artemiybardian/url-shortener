import {
  TokenPairSchema,
  UserSchema,
  UrlSchema,
  UrlListSchema,
  StatsSchema,
  type TokenPair,
  type User,
  type Url,
  type Stats,
} from "./schemas";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost";

async function request(path: string, options: RequestInit = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }

  if (res.status === 204) return null;
  return res.json();
}

function authHeaders(token: string) {
  return { Authorization: `Bearer ${token}` };
}

export async function register(
  email: string,
  password: string
): Promise<User> {
  const data = await request("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  return UserSchema.parse(data);
}

export async function login(
  email: string,
  password: string
): Promise<TokenPair> {
  const data = await request("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  return TokenPairSchema.parse(data);
}

export async function refreshToken(
  refresh_token: string
): Promise<TokenPair> {
  const data = await request("/api/auth/refresh", {
    method: "POST",
    body: JSON.stringify({ refresh_token }),
  });
  return TokenPairSchema.parse(data);
}

export async function getMe(token: string): Promise<User> {
  const data = await request("/api/auth/me", {
    headers: authHeaders(token),
  });
  return UserSchema.parse(data);
}

export async function createUrl(
  token: string,
  original_url: string,
  custom_code?: string
): Promise<Url> {
  const body: Record<string, string> = { original_url };
  if (custom_code) body.custom_code = custom_code;

  const data = await request("/api/urls/", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(body),
  });
  return UrlSchema.parse(data);
}

export async function listUrls(token: string): Promise<Url[]> {
  const data = await request("/api/urls/", {
    headers: authHeaders(token),
  });
  return UrlListSchema.parse(data);
}

export async function deleteUrl(
  token: string,
  shortCode: string
): Promise<void> {
  await request(`/api/urls/${shortCode}`, {
    method: "DELETE",
    headers: authHeaders(token),
  });
}

export async function getStats(shortCode: string): Promise<Stats> {
  const data = await request(`/api/analytics/${shortCode}/stats`);
  return StatsSchema.parse(data);
}

export function getQrUrl(shortCode: string): string {
  return `${API_BASE}/api/urls/${shortCode}/qr`;
}
