export type TrendPoint = {
  date: string
  value: number
}

const API_BASE = "/api/trends"

export async function fetchInterestOverTime(
  keywordId: number,
  countryId: number
): Promise<TrendPoint[]> {
  const res = await fetch(
    `${API_BASE}/interest-over-time?keyword_id=${keywordId}&country_id=${countryId}`
  )

  if (!res.ok) {
    throw new Error("Failed to fetch Google Trends data")
  }

  return res.json()
}
