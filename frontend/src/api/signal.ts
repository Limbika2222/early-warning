export interface SignalMetrics {
  signal_index: number
  spike_count: number
  risk_level: string
}

export interface SignalResponse {
  source: string
  metrics: SignalMetrics
  trend_data: {
    date: string
    value: number
  }[]
}

const API_BASE = import.meta.env.VITE_API_BASE

export async function fetchSignalData(
  source: string,
  diseaseId: number,
  countryId: number,
  startDate: string,
  endDate: string
): Promise<SignalResponse> {
  const params = new URLSearchParams({
    source,
    disease_id: diseaseId.toString(),
    country_id: countryId.toString(),
  })

  if (startDate) params.append("start_date", startDate)
  if (endDate) params.append("end_date", endDate)

  const res = await fetch(
    `${API_BASE}/api/signal?${params.toString()}`
  )

  if (!res.ok) {
    throw new Error("Failed to fetch signal data")
  }

  return res.json()
}