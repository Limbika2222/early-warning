export type Disease =
  | "Influenza"
  | "Malaria"
  | "Cholera"
  | "Zika"

export interface DashboardDataPoint {
  date: string
  cases: number
  trends: number
  disease: Disease
}

export const dashboardMockData: DashboardDataPoint[] = [
  // Influenza
  { date: "Jan", cases: 120, trends: 30, disease: "Influenza" },
  { date: "Feb", cases: 180, trends: 55, disease: "Influenza" },
  { date: "Mar", cases: 260, trends: 80, disease: "Influenza" },
  { date: "Apr", cases: 410, trends: 120, disease: "Influenza" },

  // Malaria
  { date: "Jan", cases: 300, trends: 20, disease: "Malaria" },
  { date: "Feb", cases: 420, trends: 35, disease: "Malaria" },
  { date: "Mar", cases: 510, trends: 60, disease: "Malaria" },
  { date: "Apr", cases: 680, trends: 95, disease: "Malaria" },

  // Cholera
  { date: "Jan", cases: 40, trends: 10, disease: "Cholera" },
  { date: "Feb", cases: 70, trends: 25, disease: "Cholera" },
  { date: "Mar", cases: 130, trends: 55, disease: "Cholera" },
  { date: "Apr", cases: 260, trends: 90, disease: "Cholera" },

  // Zika
  { date: "Jan", cases: 15, trends: 5, disease: "Zika" },
  { date: "Feb", cases: 30, trends: 15, disease: "Zika" },
  { date: "Mar", cases: 60, trends: 40, disease: "Zika" },
  { date: "Apr", cases: 110, trends: 70, disease: "Zika" },
]
