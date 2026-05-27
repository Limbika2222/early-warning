"use client";

import { useEffect, useState } from "react";

import { motion } from "framer-motion";

import {
  Activity,
  AlertTriangle,
  Brain,
  TrendingUp,
  ShieldAlert,
  RefreshCcw,
} from "lucide-react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  LineChart,
  Line,
} from "recharts";

// =====================================================
// TYPES
// =====================================================

interface TimeSeriesItem {
  date: string;
  symptom: string;
  count: number;
}

interface Alert {
  date: string;
  symptom: string;
  actual: number;
  expected: number;
  z_score: number;
  type: string;
  generated_at?: string;
}

interface Post {
  id: string;
  title: string;
  text: string;
  created_date: string;
  subreddit: string;
}

interface Metrics {
  signal_index: number;
  active_symptoms: number;
  alerts: number;
  top_symptom: string;
}

interface RedditResponse {
  time_series: TimeSeriesItem[];
  alerts: Alert[];
  alert_history?: Alert[];
  metrics: Metrics;
  posts: Post[];
  probable_diseases?: Disease[];
}

interface ChartData {
  name: string;
  value: number;
}

interface Disease {
  disease: string;
  probability: number;
}

interface MultiLineDataItem {
  date: string;
  fever?: number;
  cough?: number;
  fatigue?: number;
  headache?: number;
  chills?: number;
}

// =====================================================
// COMPONENT
// =====================================================

export default function RedditDashboard() {

  const [barData, setBarData] =
    useState<ChartData[]>([]);

  const [lineData, setLineData] =
    useState<MultiLineDataItem[]>([]);

  const [metrics, setMetrics] =
    useState<Metrics | null>(null);

  const [alerts, setAlerts] =
    useState<Alert[]>([]);

  const [, setAlertHistory] =
    useState<Alert[]>([]);

  const [posts, setPosts] =
    useState<Post[]>([]);

  const [diseases, setDiseases] =
    useState<Disease[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [lastUpdated, setLastUpdated] =
    useState<string>("");

  const [startDate, setStartDate] =
    useState<string>("");

  const [endDate, setEndDate] =
    useState<string>("");

  // =====================================================
  // FETCH DATA
  // =====================================================

  const fetchData = async () => {

    try {

      setLoading(true);

      const query =
        new URLSearchParams();

      if (startDate) {

        query.append(
          "start_date",
          startDate
        );
      }

      if (endDate) {

        query.append(
          "end_date",
          endDate
        );
      }

      const res = await fetch(
        `${import.meta.env.VITE_API_BASE}/api/reddit/signal?${query.toString()}`
      );

      const json: RedditResponse =
        await res.json();

      setDiseases(
        json.probable_diseases || []
      );

      const baseSeries =
        json.time_series;

      const symptomCounts:
        Record<string, number> = {};

      baseSeries.forEach((item) => {

        symptomCounts[item.symptom] =
          (symptomCounts[item.symptom] || 0)
          + item.count;
      });

      const formattedBar =
        Object.entries(symptomCounts)
          .map(([symptom, count]) => ({
            name: symptom,
            value: count,
          }))
          .sort((a, b) =>
            b.value - a.value
          )
          .slice(0, 6);

      setBarData(formattedBar);

      const trendMap:
        Record<string, MultiLineDataItem> = {};

      baseSeries.forEach((item) => {

        if (!trendMap[item.date]) {

          trendMap[item.date] = {
            date: item.date,
          };
        }

        const key = item.symptom;

        (
          trendMap[item.date] as unknown as Record<
            string,
            number | string
          >
        )[key] = item.count;
      });

      setLineData(
        Object.values(trendMap)
      );

      setMetrics(json.metrics);

      setAlerts(json.alerts);

      setAlertHistory(
        json.alert_history || []
      );

      setPosts(json.posts);

      setLastUpdated(
        new Date().toLocaleString()
      );

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  // =====================================================
  // EFFECT
  // =====================================================

  useEffect(() => {

    fetchData();

    // eslint-disable-next-line
  }, [startDate, endDate]);

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
        Loading Reddit Intelligence...
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
            Reddit Intelligence Dashboard
          </h1>

          <p
            className="
              text-gray-500
              mt-2
              text-lg
            "
          >
            AI-powered Reddit symptom
            surveillance and anomaly tracking
          </p>

<p
  className="
    text-sm
    text-gray-400
    mt-2
  "
>
  Last Updated: {lastUpdated || "—"}
</p>

        </div>

        <div
          className="
            flex
            items-center
            gap-4
            flex-wrap
          "
        >

          <input
            type="date"
            value={startDate}
            onChange={(e) =>
              setStartDate(
                e.target.value
              )
            }
            className="
              bg-white
              border
              border-gray-200
              rounded-2xl
              px-4
              py-3
              shadow-sm
            "
          />

          <input
            type="date"
            value={endDate}
            onChange={(e) =>
              setEndDate(
                e.target.value
              )
            }
            className="
              bg-white
              border
              border-gray-200
              rounded-2xl
              px-4
              py-3
              shadow-sm
            "
          />

          <button
            onClick={fetchData}
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

            Refresh

          </button>

        </div>

      </div>

      {/* ================================================= */}
      {/* METRIC CARDS */}
      {/* ================================================= */}

      {metrics && (

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
            title="Signal Index"
            value={metrics.signal_index}
            icon={<TrendingUp size={22} />}
            bgColor="
              bg-gradient-to-br
              from-indigo-500
              to-indigo-700
            "
          />

          <MetricCard
            title="Active Symptoms"
            value={metrics.active_symptoms}
            icon={<Activity size={22} />}
            bgColor="
              bg-gradient-to-br
              from-cyan-500
              to-blue-600
            "
          />

          <MetricCard
            title="Current Alerts"
            value={metrics.alerts}
            icon={<AlertTriangle size={22} />}
            bgColor="
              bg-gradient-to-br
              from-red-500
              to-rose-600
            "
          />

          <MetricCard
            title="Top Symptom"
            value={metrics.top_symptom}
            icon={<Brain size={22} />}
            bgColor="
              bg-gradient-to-br
              from-emerald-500
              to-green-600
            "
          />

        </div>
      )}

      {/* ================================================= */}
      {/* CHARTS */}
      {/* ================================================= */}

      <div
        className="
          grid
          grid-cols-1
          xl:grid-cols-2
          gap-8
          mb-10
        "
      >

        {/* LINE CHART */}

        <GlassCard
          title="Symptom Trends"
        >

          <div className="h-[320px]">

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <LineChart data={lineData}>

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis dataKey="date" />

                <YAxis />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="fever"
                  stroke="#EF4444"
                  strokeWidth={3}
                  dot={false}
                />

                <Line
                  type="monotone"
                  dataKey="cough"
                  stroke="#F59E0B"
                  strokeWidth={3}
                  dot={false}
                />

                <Line
                  type="monotone"
                  dataKey="fatigue"
                  stroke="#6366F1"
                  strokeWidth={3}
                  dot={false}
                />

              </LineChart>

            </ResponsiveContainer>

          </div>

        </GlassCard>

        {/* BAR CHART */}

        <GlassCard
          title="Symptom Ranking"
        >

          <div className="h-[320px]">

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <BarChart data={barData}>

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis dataKey="name" />

                <YAxis />

                <Tooltip />

                <Bar
                  dataKey="value"
                  fill="#6366F1"
                  radius={[8, 8, 0, 0]}
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </GlassCard>

      </div>

      {/* ================================================= */}
      {/* DISEASES + ALERTS */}
      {/* ================================================= */}

      <div
        className="
          grid
          grid-cols-1
          xl:grid-cols-3
          gap-8
          mb-10
        "
      >

        {/* DISEASES */}

        <GlassCard
          title="Probable Diseases"
        >

          <div className="space-y-3">

            {diseases.map((disease, index) => (

              <div key={index}>

                <div
                  className="
                    flex
                    justify-between
                    mb-1
                  "
                >

                  <span
                    className="
                      font-medium
                      text-gray-600
                      text-sm
                    "
                  >
                    {disease.disease}
                  </span>

                  <span
                    className="
                      text-sm
                      text-gray-500
                    "
                  >
                    {(
                      disease.probability * 100
                    ).toFixed(0)}
                    %
                  </span>

                </div>

                <div
                  className="
                    w-full
                    bg-gray-200
                    rounded-full
                    h-2
                  "
                >

                  <div
                    className="
                      h-2
                      bg-indigo-600
                      rounded-full
                    "
                    style={{
                      width:
                        `${disease.probability * 100}%`,
                    }}
                  />

                </div>

              </div>
            ))}

          </div>

        </GlassCard>

        {/* ALERTS */}

        <GlassCard
          title="Current Alerts"
        >

          <div className="space-y-3">

            {alerts.length === 0 ? (

              <p
                className="
                  text-gray-400
                "
              >
                No alerts detected
              </p>

            ) : (

              alerts.map((alert, index) => (

                <motion.div

                  key={index}

                  initial={{
                    opacity: 0,
                    y: 10,
                  }}

                  animate={{
                    opacity: 1,
                    y: 0,
                  }}

                  className="
                    bg-red-50
                    border
                    border-red-200
                    rounded-xl
                    p-3
                  "
                >

                  <div
                    className="
                      flex
                      items-center
                      justify-between
                    "
                  >

                    <div>

                      <h3
                        className="
                          font-semibold
                          text-red-600
                          text-sm
                        "
                      >
                        {alert.symptom.toUpperCase()}
                      </h3>

                      <p
                        className="
                          text-xs
                          text-red-500
                          mt-1
                        "
                      >
                        Spike detected on
                        {` ${alert.date}`}
                      </p>

                    </div>

                    <ShieldAlert
                      size={18}
                      className="
                        text-red-500
                      "
                    />

                  </div>

                </motion.div>
              ))
            )}

          </div>

        </GlassCard>

      </div>

      {/* ================================================= */}
      {/* POSTS */}
      {/* ================================================= */}

      <GlassCard
        title="Recent Reddit Posts"
      >

        <div className="space-y-2">

          {posts.map((post) => (

            <div

              key={post.id}

              className="
                border
                border-gray-200
                rounded-xl
                p-3
                hover:bg-gray-50
                transition-all
              "
            >

              <div
                className="
                  flex
                  items-start
                  justify-between
                  gap-3
                "
              >

                <div>

                  <h3
                    className="
                      font-semibold
                      text-gray-800
                      text-sm
                    "
                  >
                    {post.title}
                  </h3>

                  <p
                    className="
                      text-xs
                      text-gray-500
                      mt-1
                    "
                  >
                    r/{post.subreddit}
                    {" • "}
                    {post.created_date}
                  </p>

                </div>

                <span
                  className="
                    bg-indigo-100
                    text-indigo-700
                    px-2.5
                    py-0.5
                    rounded-full
                    text-xs
                    font-medium
                  "
                >
                  Reddit
                </span>

              </div>

              <p
                className="
                  text-gray-600
                  mt-2
                  text-sm
                  leading-normal
                "
              >
                {post.text?.slice(0, 180)}...
              </p>

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

    <motion.div

      whileHover={{
        y: -5,
        scale: 1.02,
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
      "
    >

      <h2
        className="
          text-xl
          font-semibold
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