// ==============================
// Types
// ==============================

// 🔥 Raw backend response (can have value OR interest)
interface RawTrendPoint {
  date: string
  value?: number
  interest?: number
  ewma?: number
  ucl?: number
  is_spike?: boolean
}

// ✅ Clean frontend type (strict)
export interface TrendPoint {
  date: string
  interest: number
  change?: number
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

export interface AnalysisResponse {
  status: string
  message: string
  output?: string
}

// ==============================
// API Base URL
// ==============================

const API_BASE = import.meta.env.VITE_API_BASE as string

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
    console.error("❌ API Error:", text)
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

  // 👇 Use RAW type here
  const res = await fetchJSON<{
    source: string
    metrics: SignalMetrics
    trend_data: RawTrendPoint[]
  }>(url)

  // 🔥 SAFE TRANSFORMATION (NO any)
  const fixedTrendData: TrendPoint[] = res.trend_data.map(
    (d: RawTrendPoint) => ({
      date: d.date,
      interest: d.interest ?? d.value ?? 0,
      ewma: d.ewma,
      ucl: d.ucl,
      is_spike: d.is_spike,
    })
  )

  return {
    ...res,
    trend_data: fixedTrendData,
  }
}

// ==============================
// Analysis Endpoints
// ==============================

export async function runAnalysis(): Promise<AnalysisResponse> {
  return fetchJSON<AnalysisResponse>(
    `${API_BASE}/api/analysis/run`,
    { method: "POST" }
  )
}

// ==============================
// Other APIs
// ==============================

export async function getSymptoms(): Promise<unknown> {
  return fetchJSON(`${API_BASE}/api/analysis/symptoms`)
}

export async function getDiseases(): Promise<unknown> {
  return fetchJSON(`${API_BASE}/api/analysis/diseases`)
}

export async function getAlerts(): Promise<unknown> {
  return fetchJSON(`${API_BASE}/api/alerts`)
}