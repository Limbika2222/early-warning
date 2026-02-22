import { useState } from "react"
import { motion } from "framer-motion"

import DiseaseSelector from "../components/dashboard/DiseaseSelector"
import ChartsGrid from "../components/dashboard/ChartsGrid"
import DashboardUploadSelector from "../components/dashboard/DashboardUploadSelector"
import MetricCard from "../components/dashboard/MetricCard"
import DateRangeSelector from "../components/dashboard/DateRangeSelector"
import DataSourceSelector, {
  type DataSource,
} from "../components/dashboard/DataSourceSelector"

import type { UploadHistoryItem } from "../api/trends"

export default function Dashboard() {
  // ================= CORE STATE =================
  const [selectedDiseaseId, setSelectedDiseaseId] = useState<number>(1)
  const [countryId, setCountryId] = useState<number>(1)
  const [dataSource, setDataSource] = useState<DataSource>("google")

  // ================= DATE STATE =================
  const [startDate, setStartDate] = useState<string | null>(null)
  const [endDate, setEndDate] = useState<string | null>(null)

  // ================= DYNAMIC METRICS =================
  const [signalIndex, setSignalIndex] = useState<number>(0)
  const [spikeCount, setSpikeCount] = useState<number>(0)
  const [riskLevel, setRiskLevel] = useState<string>("No Data")

  // ================= MAPPINGS =================
  const diseaseMap: Record<string, number> = {
    "fever cough": 1,
    malaria: 2,
    cholera: 3,
    zika: 4,
  }

  const countryMap: Record<string, number> = {
    India: 1,
    Malawi: 4,
    Philippines: 5,
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-8"
    >

      {/* ================= UPLOAD SELECTOR ================= */}
      <div className="bg-white/50 backdrop-blur-md rounded-2xl p-6 border border-white/40 shadow-md">
        <DashboardUploadSelector
          onSelect={(upload: UploadHistoryItem) => {
            const diseaseId = diseaseMap[upload.keyword]
            const selectedCountryId = countryMap[upload.country]

            if (diseaseId) setSelectedDiseaseId(diseaseId)
            if (selectedCountryId) setCountryId(selectedCountryId)
          }}
        />
      </div>

      {/* ================= METRICS ================= */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard title="Signal Index" value={signalIndex.toString()} />
        <MetricCard title="Spikes Detected" value={spikeCount.toString()} />
        <MetricCard title="Risk Level" value={riskLevel} />
      </div>

      {/* ================= DATA SOURCE ================= */}
      <div className="flex justify-center">
        <DataSourceSelector
          value={dataSource}
          onChange={setDataSource}
        />
      </div>

      {/* ================= DISEASE SELECTOR ================= */}
      <div className="bg-white/50 backdrop-blur-md rounded-2xl p-6 border border-white/40 shadow-md">
        <DiseaseSelector
          selectedDiseaseId={selectedDiseaseId}
          onSelect={setSelectedDiseaseId}
        />
      </div>

      {/* ================= DATE RANGE ================= */}
      <div className="flex justify-end">
        <DateRangeSelector
          startDate={startDate}
          endDate={endDate}
          onChange={({ startDate, endDate }) => {
            setStartDate(startDate)
            setEndDate(endDate)
          }}
        />
      </div>

      {/* ================= CHARTS ================= */}
      <div className="bg-white/50 backdrop-blur-md rounded-2xl p-8 border border-white/40 shadow-md">
        <ChartsGrid
          source={dataSource}
          diseaseId={selectedDiseaseId}
          countryId={countryId}
          startDate={startDate || undefined}
          endDate={endDate || undefined}
          onMetricsChange={(metrics) => {
            setSignalIndex(metrics.signalIndex)
            setSpikeCount(metrics.spikeCount)
            setRiskLevel(metrics.riskLevel)
          }}
        />
      </div>

    </motion.div>
  )
}