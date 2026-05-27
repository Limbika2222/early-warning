import { useEffect, useMemo, useState } from "react";

import { motion } from "framer-motion";

import {
  Activity,
  AlertTriangle,
  Globe2,
  ShieldAlert,
  TrendingUp,
  Radar,
} from "lucide-react";

import { getLiveAlerts } from "../api/alerts";

import type { Alert } from "../api/alerts";

export default function Alerts() {

  const [alerts, setAlerts] =
    useState<Alert[]>([]);

  const [loading, setLoading] =
    useState(true);

  // =====================================================
  // LOAD ALERTS
  // =====================================================

  useEffect(() => {

    async function loadAlerts() {

      try {

        const data =
          await getLiveAlerts();

        setAlerts(data);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);
      }
    }

    // Initial load

    loadAlerts();

    // Auto refresh every 15 mins

    const interval = setInterval(() => {

      loadAlerts();

    }, 15 * 60 * 1000);

    return () => clearInterval(interval);

  }, []);

  // =====================================================
  // METRICS
  // =====================================================

  const metrics = useMemo(() => {

    const critical =
      alerts.filter(
        (a) => a.severity === "CRITICAL"
      ).length;

    const countries =
      new Set(
        alerts.map((a) => a.country)
      ).size;

    const avgAnomaly =
      alerts.length > 0
        ? (
            alerts.reduce(
              (acc, curr) =>
                acc + curr.anomaly_score,
              0
            ) / alerts.length
          ).toFixed(1)
        : "0";

    return {

      total: alerts.length,

      critical,

      countries,

      avgAnomaly,
    };

  }, [alerts]);

  // =====================================================
  // SEVERITY COLORS
  // =====================================================

  const getSeverityStyle = (
    severity: string
  ) => {

    switch (severity) {

      case "CRITICAL":

        return (
          "bg-red-100 " +
          "text-red-700 " +
          "border border-red-200"
        );

      case "HIGH":

        return (
          "bg-orange-100 " +
          "text-orange-700 " +
          "border border-orange-200"
        );

      case "MEDIUM":

        return (
          "bg-yellow-100 " +
          "text-yellow-700 " +
          "border border-yellow-200"
        );

      default:

        return (
          "bg-emerald-100 " +
          "text-emerald-700 " +
          "border border-emerald-200"
        );
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
        Loading Alerts Dashboard...
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
          md:flex-row
          md:items-center
          md:justify-between
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
            Alerts & Anomalies
          </h1>

          <p
            className="
              text-gray-500
              mt-2
              text-lg
            "
          >
            Real-time outbreak intelligence
            and anomaly monitoring system
          </p>

        </div>

        <div
          className="
            flex
            items-center
            gap-3
            bg-white
            border
            border-gray-200
            px-5
            py-3
            rounded-2xl
            shadow-sm
          "
        >

          <div
            className="
              w-10
              h-10
              rounded-xl
              bg-cyan-100
              flex
              items-center
              justify-center
            "
          >
            <Radar
              size={20}
              className="
                text-cyan-700
              "
            />
          </div>

          <div>

            <p
              className="
                text-sm
                text-gray-500
              "
            >
              Monitoring Status
            </p>

            <p
              className="
                font-semibold
                text-emerald-600
              "
            >
              Live Monitoring Active
            </p>

          </div>

        </div>

      </div>

      {/* ================================================= */}
      {/* METRICS */}
      {/* ================================================= */}

      <div
        className="
          grid
          grid-cols-1
          md:grid-cols-2
          xl:grid-cols-4
          gap-6
          mb-10
        "
      >

        <MetricCard
          title="Active Alerts"
          value={metrics.total}
          icon={
            <AlertTriangle size={22} />
          }
          bgColor="
            bg-gradient-to-br
            from-red-500
            to-rose-600
          "
        />

        <MetricCard
          title="Critical Signals"
          value={metrics.critical}
          icon={
            <ShieldAlert size={22} />
          }
          bgColor="
            bg-gradient-to-br
            from-orange-500
            to-amber-600
          "
        />

        <MetricCard
          title="Countries Under Watch"
          value={metrics.countries}
          icon={
            <Globe2 size={22} />
          }
          bgColor="
            bg-gradient-to-br
            from-cyan-500
            to-blue-600
          "
        />

        <MetricCard
          title="Average Anomaly"
          value={metrics.avgAnomaly}
          icon={
            <TrendingUp size={22} />
          }
          bgColor="
            bg-gradient-to-br
            from-emerald-500
            to-green-600
          "
        />

      </div>

      {/* ================================================= */}
      {/* TABLE SECTION */}
      {/* ================================================= */}

      <div
        className="
          bg-white
          rounded-3xl
          border
          border-gray-200
          shadow-sm
          overflow-hidden
        "
      >

        {/* ================================================= */}
        {/* TABLE HEADER */}
        {/* ================================================= */}

        <div
          className="
            px-8
            py-6
            border-b
            border-gray-200
            flex
            flex-col
            md:flex-row
            md:items-center
            md:justify-between
            gap-4
          "
        >

          <div>

            <h2
              className="
                text-2xl
                font-semibold
                text-gray-900
              "
            >
              Live Alert Feed
            </h2>

            <p
              className="
                text-gray-500
                mt-1
              "
            >
              AI-powered outbreak anomaly
              detection across multiple data
              sources
            </p>

          </div>

          <div
            className="
              flex
              items-center
              gap-2
              text-sm
              text-gray-500
            "
          >

            <Activity
              size={16}
              className="
                text-emerald-500
              "
            />

            System Active

          </div>

        </div>

        {/* ================================================= */}
        {/* TABLE */}
        {/* ================================================= */}

        <div
          className="
            overflow-x-auto
          "
        >

          <table className="w-full">

            <thead
              className="
                bg-gray-50
              "
            >

              <tr
                className="
                  text-left
                  text-sm
                  text-gray-500
                "
              >

                <th className="px-8 py-4">
                  Disease
                </th>

                <th className="px-8 py-4">
                  Country
                </th>

                <th className="px-8 py-4">
                  Source
                </th>

                <th className="px-8 py-4">
                  Risk Score
                </th>

                <th className="px-8 py-4">
                  Anomaly Score
                </th>

                <th className="px-8 py-4">
                  Severity
                </th>

                <th className="px-8 py-4">
                  Status
                </th>

              </tr>

            </thead>

            <tbody>

              {alerts.map((alert, index) => (

                <motion.tr

                  key={alert.id}

                  initial={{
                    opacity: 0,
                    y: 10,
                  }}

                  animate={{
                    opacity: 1,
                    y: 0,
                  }}

                  transition={{
                    delay: index * 0.03,
                  }}

                  className="
                    border-b
                    border-gray-100
                    hover:bg-gray-50
                    transition-all
                  "
                >

                  <td className="px-8 py-5">

                    <div>

                      <div
                        className="
                          font-semibold
                          text-gray-900
                        "
                      >
                        {alert.disease}
                      </div>

                      <div
                        className="
                          text-xs
                          text-gray-400
                          mt-1
                        "
                      >
                        {new Date(
                          alert.created_at
                        ).toLocaleString()}
                      </div>

                    </div>

                  </td>

                  <td
                    className="
                      px-8
                      py-5
                      text-gray-700
                    "
                  >
                    {alert.country}
                  </td>

                  <td className="px-8 py-5">

                    <span
                      className="
                        px-3
                        py-1
                        rounded-full
                        bg-cyan-100
                        text-cyan-700
                        text-xs
                        font-medium
                      "
                    >
                      {alert.source}
                    </span>

                  </td>

                  <td className="px-8 py-5">

                    <span
                      className="
                        font-semibold
                        text-gray-900
                      "
                    >
                      {alert.risk_score}
                    </span>

                  </td>

                  <td className="px-8 py-5">

                    <span
                      className="
                        font-semibold
                        text-orange-600
                      "
                    >
                      {alert.anomaly_score}
                    </span>

                  </td>

                  <td className="px-8 py-5">

                    <span
                      className={`
                        px-3
                        py-1
                        rounded-full
                        text-xs
                        font-semibold
                        ${getSeverityStyle(
                          alert.severity
                        )}
                      `}
                    >
                      {alert.severity}
                    </span>

                  </td>

                  <td className="px-8 py-5">

                    <span
                      className="
                        text-emerald-600
                        font-medium
                        text-sm
                      "
                    >
                      {alert.status}
                    </span>

                  </td>

                </motion.tr>
              ))}

            </tbody>

          </table>

        </div>

      </div>

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

    <motion.div

      whileHover={{
        y: -6,
        scale: 1.02,
      }}

      transition={{
        duration: 0.2,
      }}

      className={`
        relative
        overflow-hidden
        rounded-3xl
        p-6
        shadow-lg
        text-white
        ${bgColor}
      `}
    >

      {/* Glow Effect */}

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

          <p
            className="
              text-sm
              text-white/80
              mb-2
            "
          >
            {title}
          </p>

          <h3
            className="
              text-4xl
              font-bold
              tracking-tight
            "
          >
            {value}
          </h3>

        </div>

        <div
          className="
            w-14
            h-14
            rounded-2xl
            bg-white/20
            backdrop-blur-md
            flex
            items-center
            justify-center
          "
        >
          {icon}
        </div>

      </div>

    </motion.div>
  );
}