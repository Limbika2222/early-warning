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
// FETCH LIVE PREDICTIONS
// =====================================================

export async function
fetchPredictions():

Promise<PredictionResponse> {

  const response = await fetch(

    `${API_BASE}/api/predictions/live`
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
// =====================================================

export async function
fetchHighRiskPredictions():

Promise<PredictionResponse> {

  const response = await fetch(

    `${API_BASE}/api/predictions/high-risk`
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
// =====================================================

export async function fetchSeasonality() {

  const response = await fetch(

    `${import.meta.env.VITE_API_BASE}/api/predictions/seasonality`
  )

  return response.json()
}
