import { useEffect, useState } from "react";

import { formatDistanceToNow } from "date-fns";

import axios from "axios";

import {

  Activity,
  Globe,
  ShieldAlert,
  RefreshCcw,

} from "lucide-react";

import {

  fetchOutbreakHistory,
  fetchDiseaseSummary,
  fetchCountrySummary,

} from "../api/who";

import type {

  WhoReport,
  DiseaseSummary,
  CountrySummary,

} from "../api/who";

import OutbreakMap from "../components/who/OutbreakMap";

// =====================================================
// API
// =====================================================

const RAW_BASE =
  import.meta.env.VITE_API_BASE;

if (!RAW_BASE) {

  throw new Error(
    "VITE_API_BASE missing"
  );
}

const CLEAN_BASE =
  RAW_BASE.endsWith("/")
    ? RAW_BASE.slice(0, -1)
    : RAW_BASE;

const API_BASE =
  `${CLEAN_BASE}`;

// =====================================================
// SEVERITY COLORS
// =====================================================

function getSeverityClasses(
  severity: string
) {

  switch (severity) {

    case "CRITICAL":

      return `
        bg-red-100
        text-red-700
        border border-red-200
      `;

    case "HIGH":

      return `
        bg-orange-100
        text-orange-700
        border border-orange-200
      `;

    case "MEDIUM":

      return `
        bg-yellow-100
        text-yellow-700
        border border-yellow-200
      `;

    default:

      return `
        bg-blue-100
        text-blue-700
        border border-blue-200
      `;
  }
}

// =====================================================
// TIME FORMAT
// =====================================================

function formatRelativeTime(
  dateString?: string
) {

  if (!dateString) {

    return "Unknown time";
  }

  try {

    const parsedDate =
      new Date(dateString);

    return formatDistanceToNow(
      parsedDate,
      {
        addSuffix: true,
      }
    );

  } catch {

    return "Unknown time";
  }
}

// =====================================================
// COMPONENT
// =====================================================

export default function WhoDashboard() {

  const [reports, setReports] =
    useState<WhoReport[]>([]);

  const [diseases, setDiseases] =
    useState<DiseaseSummary[]>([]);

  const [countries, setCountries] =
    useState<CountrySummary[]>([]);

  const [

    countryDiseases,
    setCountryDiseases,

  ] = useState<
    Record<string, string[]>
  >({});

  const [loading, setLoading] =
    useState(true);

  // =====================================================
  // LOAD DASHBOARD
  // =====================================================

  async function loadDashboard() {

    try {

      setLoading(true);

      const [

        history,
        diseaseSummary,
        countrySummary,

      ] = await Promise.all([

        fetchOutbreakHistory(),

        fetchDiseaseSummary(),

        fetchCountrySummary(),
      ]);

      const reportsData =
        history.reports;

      const diseaseMap:
        Record<string, Set<string>> = {};

      reportsData.forEach(
        (report) => {

          const iso2 =
            report.country.iso2;

          if (!iso2) return;

          if (!diseaseMap[iso2]) {

            diseaseMap[iso2] =
              new Set();
          }

          diseaseMap[iso2].add(
            report.disease
          );
        }
      );

      const finalMap:
        Record<string, string[]> = {};

      Object.entries(diseaseMap)
        .forEach(([iso2, diseases]) => {

          finalMap[iso2] =
            Array.from(diseases);
        });

      setCountryDiseases(
        finalMap
      );

      setReports(history.reports);

      setDiseases(
        diseaseSummary.diseases
      );

      setCountries(
        countrySummary.countries
      );

    } catch (err) {

      console.error(
        "WHO dashboard error:",
        err
      );

    } finally {

      setLoading(false);
    }
  }

  // =====================================================
  // EFFECT
  // =====================================================

  useEffect(() => {

    loadDashboard();

  }, []);

  // =====================================================
  // REFRESH
  // =====================================================

  const refreshWHOData =
    async () => {

      try {

        setLoading(true);

        await axios.post(
          `${API_BASE}/api/who/refresh`
        );

        await loadDashboard();

      } catch (error) {

        console.error(
          "WHO refresh failed",
          error
        );

      } finally {

        setLoading(false);
      }
    };

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {

    return (

      <div
        className="
          min-h-screen
          bg-gray-50
          flex
          items-center
          justify-center
          text-gray-500
        "
      >
        Loading WHO intelligence...
      </div>
    );
  }

  // =====================================================
  // UI
  // =====================================================

  return (

    <div
      className="
        min-h-screen
        bg-gray-50
        p-8
      "
    >

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <div
        className="
          flex
          flex-col
          xl:flex-row
          xl:items-center
          xl:justify-between
          gap-6
          mb-10
        "
      >

        <div>

          <h1
            className="
              text-4xl
              font-bold
              text-gray-900
              tracking-tight
            "
          >
            WHO Intelligence Dashboard
          </h1>

          <p
            className="
              text-gray-500
              mt-2
              text-lg
            "
          >
            Official outbreak surveillance
            & epidemiological intelligence
          </p>

        </div>

        <button

          onClick={refreshWHOData}

          className="
            flex
            items-center
            gap-2
            bg-indigo-600
            hover:bg-indigo-700
            text-white
            px-5
            py-3
            rounded-2xl
            transition-all
          "
        >

          <RefreshCcw size={16} />

          Refresh WHO Data

        </button>

      </div>

      {/* ================================================= */}
      {/* METRIC CARDS */}
      {/* ================================================= */}

      <div
        className="
          grid
          grid-cols-1
          md:grid-cols-3
          gap-6
          mb-10
        "
      >

        <MetricCard
          title="Total Outbreak Reports"
          value={reports.length}
          icon={<ShieldAlert size={22} />}
          bgColor="
            bg-gradient-to-br
            from-red-500
            to-rose-600
          "
        />

        <MetricCard
          title="Diseases Detected"
          value={diseases.length}
          icon={<Activity size={22} />}
          bgColor="
            bg-gradient-to-br
            from-indigo-500
            to-indigo-700
          "
        />

        <MetricCard
          title="Countries Affected"
          value={countries.length}
          icon={<Globe size={22} />}
          bgColor="
            bg-gradient-to-br
            from-emerald-500
            to-green-600
          "
        />

      </div>

      {/* ================================================= */}
      {/* MAP */}
      {/* ================================================= */}

      <GlassCard
        title="Global Outbreak Map"
      >

        <OutbreakMap
          countries={countries}
          diseaseMap={countryDiseases}
        />

      </GlassCard>

      {/* ================================================= */}
      {/* SUMMARY GRID */}
      {/* ================================================= */}

      <div
        className="
          grid
          grid-cols-1
          xl:grid-cols-2
          gap-8
          mt-10
        "
      >

        {/* DISEASE SUMMARY */}

        <GlassCard
          title="Disease Rankings"
        >

          <div className="space-y-4">

            {diseases.map((disease) => (

              <div

                key={disease.disease}

                className="
                  border
                  border-gray-200
                  rounded-2xl
                  px-5
                  py-4
                  hover:bg-gray-50
                  transition-all
                "
              >

                <div
                  className="
                    flex
                    justify-between
                    items-center
                  "
                >

                  <span
                    className="
                      font-semibold
                      text-gray-800
                    "
                  >
                    {disease.disease}
                  </span>

                  <span
                    className="
                      bg-indigo-100
                      text-indigo-700
                      px-4
                      py-1
                      rounded-full
                      text-sm
                      font-semibold
                    "
                  >
                    {disease.count}
                  </span>

                </div>

              </div>
            ))}

          </div>

        </GlassCard>

        {/* COUNTRY SUMMARY */}

        <GlassCard
          title="Country Outbreak Summary"
        >

          <div className="space-y-4">

            {countries.map((country) => (

              <div

                key={country.country_iso2}

                className="
                  border
                  border-gray-200
                  rounded-2xl
                  px-5
                  py-4
                  hover:bg-gray-50
                  transition-all
                "
              >

                <div
                  className="
                    flex
                    justify-between
                    items-center
                  "
                >

                  <div
                    className="
                      flex
                      items-center
                      gap-3
                    "
                  >

                    <span
                      className="
                        font-semibold
                        text-gray-800
                      "
                    >
                      {country.country_name || "Unknown"}
                    </span>

                    <span
                      className="
                        bg-gray-100
                        text-gray-500
                        px-2
                        py-1
                        rounded-full
                        text-xs
                      "
                    >
                      {country.country_iso2}
                    </span>

                  </div>

                  <span
                    className="
                      bg-emerald-100
                      text-emerald-700
                      px-4
                      py-1
                      rounded-full
                      text-sm
                      font-semibold
                    "
                  >
                    {country.outbreak_count}
                  </span>

                </div>

              </div>
            ))}

          </div>

        </GlassCard>

      </div>

      {/* ================================================= */}
      {/* OUTBREAK FEED */}
      {/* ================================================= */}

      <GlassCard
        title="Historical Outbreak Feed"
      >

        <div className="space-y-5">

          {reports.map((report) => (

            <div

              key={report.url}

              className="
                border
                border-gray-200
                rounded-3xl
                p-6
                bg-white
                hover:shadow-md
                transition-all
              "
            >

              <div
                className="
                  flex
                  flex-col
                  xl:flex-row
                  xl:items-start
                  xl:justify-between
                  gap-6
                "
              >

                <div className="flex-1">

                  <div
                    className="
                      flex
                      items-start
                      gap-3
                      flex-wrap
                    "
                  >

                    <h3
                      className="
                        text-xl
                        font-bold
                        text-gray-900
                      "
                    >
                      {report.title}
                    </h3>

                    <span
                      className={`
                        px-3 py-1 rounded-full
                        text-xs font-bold
                        ${getSeverityClasses(
                          report.severity
                        )}
                      `}
                    >
                      {report.severity}
                    </span>

                  </div>

                  <div
                    className="
                      flex
                      flex-wrap
                      gap-3
                      mt-5
                    "
                  >

                    <Tag>
                      Disease:
                      {" "}
                      {report.disease}
                    </Tag>

                    <Tag>
                      Country:
                      {" "}
                      {report.country.name || "Unknown"}
                    </Tag>

                    <Tag>
                      Source:
                      {" "}
                      {report.source}
                    </Tag>

                    <Tag>
                      {formatRelativeTime(
                        report.ingested_at
                      )}
                    </Tag>

                  </div>

                </div>

                <a

                  href={report.url}

                  target="_blank"

                  rel="noreferrer"

                  className="
                    bg-indigo-600
                    hover:bg-indigo-700
                    text-white
                    px-5
                    py-3
                    rounded-2xl
                    text-sm
                    font-semibold
                    transition-all
                    h-fit
                  "
                >
                  Open Report
                </a>

              </div>

            </div>
          ))}

        </div>

      </GlassCard>

    </div>
  );
}

// =====================================================
// METRIC CARD
// =====================================================

function MetricCard({

  title,
  value,
  icon,
  bgColor,

}: {
  title: string;

  value: string | number;

  icon: React.ReactNode;

  bgColor: string;
}) {

  return (

    <div
      className={`
        rounded-3xl
        p-6
        text-white
        shadow-xl
        relative
        overflow-hidden
        ${bgColor}
      `}
    >

      <div
        className="
          absolute
          -top-10
          -right-10
          w-40
          h-40
          bg-white/10
          rounded-full
        "
      />

      <div
        className="
          relative
          z-10
          flex
          items-center
          justify-between
        "
      >

        <div>

          <p className="text-white/80">
            {title}
          </p>

          <h2
            className="
              text-5xl
              font-black
              mt-4
            "
          >
            {value}
          </h2>

        </div>

        <div
          className="
            w-14
            h-14
            rounded-2xl
            bg-white/20
            flex
            items-center
            justify-center
          "
        >
          {icon}
        </div>

      </div>

    </div>
  );
}

// =====================================================
// GLASS CARD
// =====================================================

function GlassCard({

  title,
  children,

}: {
  title: string;

  children: React.ReactNode;
}) {

  return (

    <div
      className="
        bg-white
        rounded-3xl
        border
        border-gray-200
        shadow-sm
        p-6
        mb-8
      "
    >

      <h2
        className="
          text-2xl
          font-bold
          text-gray-900
          mb-6
        "
      >
        {title}
      </h2>

      {children}

    </div>
  );
}

// =====================================================
// TAG
// =====================================================

function Tag({

  children,

}: {
  children: React.ReactNode;
}) {

  return (

    <span
      className="
        bg-gray-100
        text-gray-600
        px-3
        py-1
        rounded-full
        text-sm
      "
    >
      {children}
    </span>
  );
}