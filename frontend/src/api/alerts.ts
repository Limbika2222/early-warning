const API_BASE =
  import.meta.env.VITE_API_URL ||
  "https://8000-firebase-early-warning-1772198111524.cluster-fdkw7vjj7bgguspe3fbbc25tra.cloudworkstations.dev";

export interface Alert {
  id: number;

  disease: string;

  country: string;

  source: string;

  risk_score: number;

  anomaly_score: number;

  outbreak_probability: number;

  severity: string;

  trend_direction: string;

  status: string;

  message?: string;

  resolved: boolean;

  created_at: string;
}

// =====================================================
// GET LIVE ALERTS
// =====================================================

export async function getLiveAlerts(): Promise<Alert[]> {
  const response = await fetch(
    `${API_BASE}/api/alerts/live`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch live alerts"
    );
  }

  return response.json();
}

// =====================================================
// GET ALERT HISTORY
// =====================================================

export async function getAlertHistory(): Promise<Alert[]> {
  const response = await fetch(
    `${API_BASE}/api/alerts/history`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch alert history"
    );
  }

  return response.json();
}

// =====================================================
// GET COUNTRY ALERTS
// =====================================================

export async function getCountryAlerts(
  country: string
): Promise<Alert[]> {

  const response = await fetch(
    `${API_BASE}/api/alerts/country/${country}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch country alerts"
    );
  }

  return response.json();
}

// =====================================================
// GET DISEASE ALERTS
// =====================================================

export async function getDiseaseAlerts(
  disease: string
): Promise<Alert[]> {

  const response = await fetch(
    `${API_BASE}/api/alerts/disease/${disease}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch disease alerts"
    );
  }

  return response.json();
}