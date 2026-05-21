const API_BASE =
  import.meta.env.VITE_API_BASE

// =====================================================
// TYPES
// =====================================================

export interface Prediction {

  disease: string

  country: string

  google_score: number

  reddit_score: number

  who_score: number

  combined_score: number

  matched_keywords: string[]

  risk_level: string
}

export interface PredictionResponse {

  source: string

  count: number

  predictions: Prediction[]
}

// =====================================================
// SEASONALITY TYPES
// =====================================================

export interface SeasonalityResult {

  disease: string

  peak_month: string

  top_months: string[]

  seasonality_strength: number

  seasonal_risk: string
}

export interface SeasonalityResponse {

  country: string

  results: SeasonalityResult[]
}

// =====================================================
// FETCH LIVE PREDICTIONS
// COUNTRY-AWARE
// =====================================================

export async function
fetchPredictions(

  country: string = "GLOBAL"

):

Promise<PredictionResponse> {

  const response = await fetch(

    `${API_BASE}/api/predictions/live?country=${country}`
  )

  if (!response.ok) {

    throw new Error(
      "Failed to fetch predictions"
    )
  }

  return response.json()
}

// =====================================================
// FETCH HIGH RISK
// COUNTRY-AWARE
// =====================================================

export async function
fetchHighRiskPredictions(

  country: string = "GLOBAL"

):

Promise<PredictionResponse> {

  const response = await fetch(

    `${API_BASE}/api/predictions/high-risk?country=${country}`
  )

  if (!response.ok) {

    throw new Error(
      "Failed to fetch high-risk predictions"
    )
  }

  return response.json()
}

// =====================================================
// FETCH SEASONALITY
// COUNTRY-AWARE
// =====================================================

export async function
fetchSeasonality(

  country: string = "GLOBAL"

):

Promise<SeasonalityResponse> {

  const response = await fetch(

    `${API_BASE}/api/predictions/seasonality?country=${country}`
  )

  if (!response.ok) {

    throw new Error(
      "Failed to fetch seasonality data"
    )
  }

  return response.json()
}