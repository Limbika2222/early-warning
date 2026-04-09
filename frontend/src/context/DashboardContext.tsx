import { createContext, useContext, useState, useMemo } from "react"

// Types
export interface DashboardFilters {
  startDate: string
  endDate: string
  diseases: string[]
  symptoms: string[]
  country: string | null
}

// Mock data type (you will replace later with API)
export interface TrendRecord {
  date: string
  country: string
  disease: string
  symptom: string
  interest: number
  risk: string
}

// Context type
interface DashboardContextType {
  filters: DashboardFilters
  setFilters: (filters: DashboardFilters) => void
  data: TrendRecord[]
  filteredData: TrendRecord[]
}

// Create context
const DashboardContext = createContext<DashboardContextType | undefined>(undefined)

// Hook
// eslint-disable-next-line react-refresh/only-export-components
export function useDashboard() {
  const context = useContext(DashboardContext)
  if (!context) {
    throw new Error("useDashboard must be used inside DashboardProvider")
  }
  return context
}

// Provider
export function DashboardProvider({ children }: { children: React.ReactNode }) {
  // Global filters
  const [filters, setFilters] = useState<DashboardFilters>({
    startDate: "2021-01-01",
    endDate: "2021-12-31",
    diseases: [],
    symptoms: [],
    country: null,
  })

  // MOCK DATA (replace later with API)
  const [data] = useState<TrendRecord[]>([
    {
      date: "2021-05-01",
      country: "India",
      disease: "Malaria",
      symptom: "Fever",
      interest: 78,
      risk: "HIGH",
    },
    {
      date: "2021-05-01",
      country: "India",
      disease: "Flu",
      symptom: "Cough",
      interest: 65,
      risk: "MEDIUM",
    },
  ])

  // Filter engine
  const filteredData = useMemo(() => {
    return data.filter((row) => {
      return (
        row.date >= filters.startDate &&
        row.date <= filters.endDate &&
        (filters.country ? row.country === filters.country : true) &&
        (filters.diseases.length ? filters.diseases.includes(row.disease) : true) &&
        (filters.symptoms.length ? filters.symptoms.includes(row.symptom) : true)
      )
    })
  }, [data, filters])

  return (
    <DashboardContext.Provider
      value={{ filters, setFilters, data, filteredData }}
    >
      {children}
    </DashboardContext.Provider>
  )
}