const API_BASE = import.meta.env.VITE_API_BASE;

export const fetchRedditSignal = async () => {
  const res = await fetch(`${API_BASE}/api/reddit/signal`);
  return res.json();
};