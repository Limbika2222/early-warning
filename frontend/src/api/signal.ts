// ==============================
// Types
// ==============================

export interface TrendPoint {
  date: string
  value: number
  ewma?: number
  ucl?: number
  is_spike?: boolean
}

export interface SignalMetrics {
  signal_index: number
  spike_count: number
  momentum_percent?: number
  risk_level: string
}

export interface SignalResponse {
  source: string
  metrics: SignalMetrics
  trend_data: TrendPoint[]
}

// ==============================
// API Base URL
// ==============================

const API_BASE = import.meta.env.VITE_API_BASE

// ==============================
// Generic Fetch Helper
// ==============================

async function fetchJSON<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(url, options)

  if (!res.ok) {
    const text = await res.text()
    console.error("API Error:", text)
    throw new Error(`Request failed: ${res.status}`)
  }

  return res.json() as Promise<T>
}

// ==============================
// Signal API
// ==============================

export async function fetchSignalData(
  source: string,
  diseaseId: number,
  countryId: number,
  startDate?: string,
  endDate?: string
): Promise<SignalResponse> {
  const params = new URLSearchParams({
    source,
    disease_id: diseaseId.toString(),
    country_id: countryId.toString(),
  })

  if (startDate) params.append("start_date", startDate)
  if (endDate) params.append("end_date", endDate)

  const url = `${API_BASE}/api/signal?${params.toString()}`

  return fetchJSON<SignalResponse>(url)
}

// ==============================
// Analysis Endpoints
// ==============================

export async function runAnalysis(): Promise<{ message: string }> {
  return fetchJSON<{ message: string }>(
    `${API_BASE}/analysis/run`,
    {
      method: "POST",
    }
  )
}

export async function getSymptoms() {
  return fetchJSON(`${API_BASE}/analysis/symptoms`)
}

export async function getDiseases() {
  return fetchJSON(`${API_BASE}/analysis/diseases`)
}

export async function getAlerts() {
  return fetchJSON(`${API_BASE}/alerts`)
}