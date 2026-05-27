
import {
  useEffect,
  useState,
} from "react";
import { motion } from "framer-motion";
import {
  getReports,
  downloadReport,
  previewReport,
  type Report,
} from "../api/reports";
import {
  FileText,
  Calendar,
  Globe,
  TrendingUp,
} from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  bgColor: string;
}

export default function Reports() {
  const [reports, setReports] =
    useState<Report[]>([]);
  const [loading, setLoading] =
    useState(true);
  const [previewUrl, setPreviewUrl] =
    useState<string | null>(null);
  const [search, setSearch] =
    useState("");
  const [filter, setFilter] =
    useState("all");
  const [country, setCountry] =
    useState("Malawi");

  // Load reports
  async function loadReports() {
    try {
      const data =
        await getReports();
      setReports(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadReports();
  }, []);

  // Filtered reports
  const filteredReports = reports.filter(
    (report) => {
      const matchesSearch =
        report.filename
          .toLowerCase()
          .includes(
            search.toLowerCase()
          );
      const matchesFilter =
        filter === "all" ||
        report.report_type ===
        filter;
      return (
        matchesSearch &&
        matchesFilter
      );
    }
  );

  // Generate new report
  async function handleGenerate(
    type?: string
  ) {
    try {
      let endpoint =
        `${
          import.meta.env.VITE_API_BASE
        }/api/reports/weekly`;
      if (type === "monthly") {
        endpoint =
          `${
            import.meta.env.VITE_API_BASE
          }/api/reports/monthly`;
      }
      window.open(
        endpoint,
        "_blank"
      );
    } catch (error) {
      console.error(error);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center text-gray-500">
        Loading Reports Dashboard...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* HEADER */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-10">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 tracking-tight">
            Report Intelligence Center
          </h1>
          <p className="text-gray-500 mt-2 text-lg">
            AI-generated outbreak intelligence
            & predictive surveillance reports
          </p>
        </div>
      </div>

      {/* METRICS */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10">
        <MetricCard
          title="Total Reports"
          value={reports.length}
          icon={<FileText size={22} />}
          bgColor="bg-gradient-to-br from-cyan-500 to-blue-600"
        />
        <MetricCard
          title="Monthly Reports"
          value={
            reports.filter(
              (r) =>
                r.report_type ===
                "monthly"
            ).length
          }
          icon={<Calendar size={22} />}
          bgColor="bg-gradient-to-br from-purple-500 to-fuchsia-600"
        />
        <MetricCard
          title="Country Reports"
          value={
            reports.filter(
              (r) =>
                r.report_type ===
                "country"
            ).length
          }
          icon={<Globe size={22} />}
          bgColor="bg-gradient-to-br from-emerald-500 to-green-600"
        />
        <MetricCard
          title="Forecast Reports"
          value="12"
          icon={
            <TrendingUp size={22} />
          }
          bgColor="bg-gradient-to-br from-orange-500 to-amber-600"
        />
      </div>

      {/* GENERATE PANEL */}
      <div className="bg-white border border-gray-200 rounded-3xl shadow-sm p-6 mb-10">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-gray-800">
            Generate Intelligence Reports
          </h2>
          <p className="text-gray-500 mt-1 text-sm">
            Create AI-powered outbreak
            surveillance and forecasting reports
          </p>
        </div>
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
          <div className="border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition">
            <h3 className="text-lg font-semibold text-gray-800 mb-1">
              Weekly Intelligence Report
            </h3>
            <p className="text-gray-500 text-xs mb-4">
              Summary of outbreak anomalies,
              WHO surveillance,
              AI forecasting,
              and risk escalation.
            </p>
            <button
              onClick={() =>
                handleGenerate()
              }
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition text-sm"
            >
              Generate Report
            </button>
          </div>
          <div className="border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition">
            <h3 className="text-lg font-semibold text-gray-800 mb-1">
              Monthly Intelligence Report
            </h3>
            <p className="text-gray-500 text-xs mb-4">
              Long-term outbreak analysis,
              seasonal intelligence,
              and predictive epidemiology trends.
            </p>
            <button
              onClick={() =>
                window.open(
                  `${
                    import.meta.env
                      .VITE_API_BASE
                  }/api/reports/monthly`,
                  "_blank"
                )
              }
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition text-sm"
            >
              Generate Report
            </button>
          </div>
          <div className="border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition">
            <h3 className="text-lg font-semibold text-gray-800 mb-1">
              Country Intelligence Report
            </h3>
            <p className="text-gray-500 text-xs mb-4">
              Generate geo-aware outbreak
              intelligence reports
              for monitored countries.
            </p>
            <div className="flex gap-3">
              <select
                value={country}
                onChange={(e) =>
                  setCountry(
                    e.target.value
                  )
                }
                className="bg-gray-100 border border-gray-200 rounded-lg px-3 py-2 w-full outline-none focus:ring-2 focus:ring-gray-300 text-sm"
              >
                <option>Malawi</option>
                <option>India</option>
                <option>
                  South Africa
                </option>
              </select>
              <button
                onClick={() =>
                  window.open(
                    `${
                      import.meta.env
                        .VITE_API_BASE
                    }/api/reports/country/${country}`,
                    "_blank"
                  )
                }
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 rounded-lg font-medium transition text-sm"
              >
                Generate
              </button>
            </div>
          </div>
          <div className="border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition">
            <h3 className="text-lg font-semibold text-gray-800 mb-1">
              Forecast Intelligence Report
            </h3>
            <p className="text-gray-500 text-xs mb-4">
              Predictive outbreak probabilities,
              seasonal risk forecasts,
              and anomaly escalation outlooks.
            </p>
            <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition text-sm">
              Generate Forecast
            </button>
          </div>
        </div>
      </div>

      {/* REPORT HISTORY */}
      <div className="bg-white rounded-3xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-8 py-6 border-b border-gray-200 flex justify-between items-center">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">
              Report History
            </h2>
            <p className="text-gray-500 mt-1 text-sm">
              Browse and manage previously
              generated reports
            </p>
          </div>
          <div className="flex gap-4">
            <input
              type="text"
              placeholder="Search reports..."
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              className="bg-white border border-gray-200 rounded-xl px-5 py-3 shadow-sm w-[260px]"
            />
            <select
              value={filter}
              onChange={(e) =>
                setFilter(e.target.value)
              }
              className="bg-white border border-gray-200 rounded-xl px-5 py-3 shadow-sm"
            >
              <option value="all">
                All Reports
              </option>
              <option value="weekly">
                Weekly
              </option>
              <option value="monthly">
                Monthly
              </option>
              <option value="country">
                Country
              </option>
            </select>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr className="text-left text-sm text-gray-500">
                <th className="px-8 py-4 font-semibold">
                  Report
                </th>
                <th className="px-8 py-4 font-semibold">
                  Type
                </th>
                <th className="px-8 py-4 font-semibold">
                  Generated
                </th>
                <th className="px-8 py-4 font-semibold">
                  Generated By
                </th>
                <th className="px-8 py-4 font-semibold">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredReports.map(
                (report) => (
                  <tr
                    key={report.id}
                    className="border-b border-gray-100 hover:bg-gray-50 transition-all"
                  >
                    <td className="px-8 py-5 font-semibold text-gray-900">
                      {report.filename}
                    </td>
                    <td className="px-8 py-5 capitalize text-gray-700">
                      {
                        report.report_type
                      }
                    </td>
                    <td className="px-8 py-5 text-gray-700">
                      {
                        report.generated_at.split(
                          "T"
                        )[0]
                      }
                    </td>
                    <td className="px-8 py-5 text-gray-700">
                      {
                        report.generated_by
                      }
                    </td>
                    <td className="px-8 py-5">
                      <button
                        onClick={() =>
                          setPreviewUrl(
                            previewReport(
                              report.id
                            )
                          )
                        }
                        className="bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded-lg mr-2 font-medium transition text-sm"
                      >
                        Preview
                      </button>
                      <button
                        onClick={() =>
                          downloadReport(
                            report.id
                          )
                        }
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition text-sm"
                      >
                        Download
                      </button>
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* PDF PREVIEW MODAL */}
      {previewUrl && (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-6">
          <div className="bg-white rounded-3xl w-full max-w-6xl h-[90vh] relative overflow-hidden shadow-2xl border-2 border-white">
            <div className="flex items-center justify-between p-4 border-b bg-gray-50">
              <h2 className="text-2xl font-bold ml-4 text-gray-900">
                Report Preview
              </h2>
              <button
                onClick={() =>
                  setPreviewUrl(null)
                }
                className="bg-red-500 hover:bg-red-600 text-white px-5 py-3 rounded-lg font-semibold"
              >
                Close
              </button>
            </div>
            <iframe
              src={previewUrl}
              className="w-full h-full"
            />
          </div>
        </div>
      )}
    </div>
  );
}

function MetricCard({
  title,
  value,
  icon,
  bgColor,
}: MetricCardProps) {
  return (
    <motion.div
      whileHover={{
        y: -6,
        scale: 1.02,
      }}
      transition={{
        duration: 0.2,
      }}
      className={`relative overflow-hidden rounded-3xl p-6 shadow-lg text-white ${bgColor}`}
    >
      <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full" />
      <div className="relative z-10 flex items-center justify-between">
        <div>
          <p className="text-sm text-white/80 mb-2">
            {title}
          </p>
          <h3 className="text-4xl font-bold tracking-tight">
            {value}
          </h3>
        </div>
        <div className="w-14 h-14 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center">
          {icon}
        </div>
      </div>
    </motion.div>
  );
}
