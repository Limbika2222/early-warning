// =====================================================
// TYPES
// =====================================================

export interface WhoCountry {
    name: string | null
    iso2: string | null
  }
  
  export interface WhoReport {
    id?: number
    title: string
    disease: string
    severity: string
    country: {
      name: string | null
      iso2: string | null
    }
    source: string
    url: string
    published: string
    ingested_at?: string
  }
  
  export interface WhoHistoryResponse {
    source: string
    count: number
    reports: WhoReport[]
  }
  
  export interface DiseaseSummary {
    disease: string
    count: number
  }
  
  export interface CountrySummary {
    country_name: string | null
    country_iso2: string
    outbreak_count: number
  }
  
  // =====================================================
  // API BASE
  // =====================================================
  
  const RAW_BASE = import.meta.env.VITE_API_BASE
  
  if (!RAW_BASE) {
    throw new Error(
      "VITE_API_BASE missing"
    )
  }
  
  const CLEAN_BASE = RAW_BASE.endsWith("/")
    ? RAW_BASE.slice(0, -1)
    : RAW_BASE
  
  const API_BASE = `${CLEAN_BASE}/api/who`
  
  // =====================================================
  // SAFE FETCH
  // =====================================================
  
  async function safeFetch<T>(
    url: string
  ): Promise<T> {
  
    const res = await fetch(url)
  
    if (!res.ok) {
      throw new Error(
        `API error: ${res.status}`
      )
    }
  
    return res.json()
  }
  
  // =====================================================
  // LIVE OUTBREAKS
  // =====================================================
  
  export async function fetchLiveOutbreaks() {
    return safeFetch<WhoHistoryResponse>(
      `${API_BASE}/outbreaks`
    )
  }
  
  // =====================================================
  // HISTORICAL OUTBREAKS
  // =====================================================
  
  export async function fetchOutbreakHistory(
    countryIso2?: string,
    disease?: string
  ) {
  
    const params = new URLSearchParams()
  
    if (countryIso2) {
      params.set(
        "country_iso2",
        countryIso2
      )
    }
  
    if (disease) {
      params.set(
        "disease",
        disease
      )
    }
  
    return safeFetch<WhoHistoryResponse>(
      `${API_BASE}/history?${params.toString()}`
    )
  }
  
  // =====================================================
  // DISEASE SUMMARY
  // =====================================================
  
  export async function fetchDiseaseSummary() {
  
    return safeFetch<{
      count: number
      diseases: DiseaseSummary[]
    }>(
      `${API_BASE}/diseases`
    )
  }
  
  // =====================================================
  // COUNTRY SUMMARY
  // =====================================================
  
  export async function fetchCountrySummary() {
  
    return safeFetch<{
      count: number
      countries: CountrySummary[]
    }>(
      `${API_BASE}/countries`
    )
  }