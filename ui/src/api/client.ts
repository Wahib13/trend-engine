const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    ...options,
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  console.log("API Response:", res);
  return res.json();
}
