
import {
  useEffect,
  useState,
} from "react";
import {
  motion,
} from "framer-motion";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import {
  AlertTriangle,
  Globe,
  ShieldAlert,
  FileText,
  BrainCircuit,
} from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
}

interface GlassCardProps {
  title: string;
  children: React.ReactNode;
}

interface FeedItemProps {
  severity: string;
  disease: string;
  country: string;
}

interface StatusItemProps {
  label: string;
  status: string;
}

interface ReportItemProps {
  title: string;
}

const severityData = [
  { name: "LOW", value: 12 },
  { name: "MEDIUM", value: 18 },
  { name: "HIGH", value: 9 },
  { name: "CRITICAL", value: 4 },
];

const COLORS = [
  "#22C55E",
  "#FACC15",
  "#F97316",
  "#EF4444",
];

const trendData = [
  { day: "Mon", risk: 45 },
  { day: "Tue", risk: 52 },
  { day: "Wed", risk: 61 },
  { day: "Thu", risk: 70 },
  { day: "Fri", risk: 74 },
  { day: "Sat", risk: 66 },
  { day: "Sun", risk: 81 },
];

export default function CommandCenter() {
  const [currentTime, setCurrentTime] =
    useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(
        new Date().toLocaleString()
      );
    }, 1000);
    return () =>
      clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-200 p-8">
      {/* ====================================== */}
      {/* HEADER */}
      {/* ====================================== */}
      <div className="flex items-center justify-between mb-10">
        <div>
          <h1 className="text-5xl font-black text-slate-900">
            AI Command Center
          </h1>
          <p className="text-slate-600 mt-3 text-lg">
            Global outbreak intelligence
            & predictive surveillance
          </p>
        </div>
        <div className="bg-white rounded-2xl shadow-lg px-6 py-4">
          <p className="text-sm text-slate-500">
            System Time
          </p>
          <h2 className="font-bold text-slate-800">
            {currentTime}
          </h2>
        </div>
      </div>

      {/* ====================================== */}
      {/* ALERT TICKER */}
      {/* ====================================== */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-red-500 text-white rounded-2xl px-6 py-4 mb-10 shadow-xl overflow-hidden"
      >
        <div className="animate-pulse font-semibold">
          🔴 HIGH RISK:
          Influenza spike detected in India |
          🟠 MODERATE:
          Malaria anomaly detected in Malawi |
          🔴 CRITICAL:
          WHO outbreak escalation detected
        </div>
      </motion.div>

      {/* ====================================== */}
      {/* METRIC CARDS */}
      {/* ====================================== */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-10">
        <MetricCard
          title="Active Alerts"
          value="43"
          icon={<AlertTriangle />}
          color="bg-red-500"
        />
        <MetricCard
          title="Countries Under Watch"
          value="17"
          icon={<Globe />}
          color="bg-blue-500"
        />
        <MetricCard
          title="AI Forecast Accuracy"
          value="92%"
          icon={<BrainCircuit />}
          color="bg-purple-500"
        />
        <MetricCard
          title="WHO Signals"
          value="12"
          icon={<ShieldAlert />}
          color="bg-orange-500"
        />
      </div>

      {/* ====================================== */}
      {/* MAIN GRID */}
      {/* ====================================== */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* ================================== */}
        {/* LEFT SIDE */}
        {/* ================================== */}
        <div className="xl:col-span-2 space-y-8">
          {/* =============================== */}
          {/* RISK TREND */}
          {/* =============================== */}
          <GlassCard title="Global Risk Trend">
            <div className="h-[350px]">
              <ResponsiveContainer>
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="risk"
                    stroke="#2563EB"
                    strokeWidth={4}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>

          {/* =============================== */}
          {/* LIVE INTELLIGENCE */}
          {/* =============================== */}
          <GlassCard title="Live Intelligence Feed">
            <div className="space-y-5">
              <FeedItem
                severity="HIGH"
                disease="Influenza"
                country="India"
              />
              <FeedItem
                severity="MEDIUM"
                disease="Malaria"
                country="Malawi"
              />
              <FeedItem
                severity="CRITICAL"
                disease="COVID-19"
                country="South Africa"
              />
            </div>
          </GlassCard>
        </div>

        {/* ================================== */}
        {/* RIGHT SIDE */}
        {/* ================================== */}
        <div className="space-y-8">
          {/* =============================== */}
          {/* SEVERITY */}
          {/* =============================== */}
          <GlassCard title="Severity Distribution">
            <div className="h-[300px]">
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={severityData}
                    dataKey="value"
                    outerRadius={100}
                    innerRadius={60}
                  >
                    {severityData.map(
                      (_, index) => (
                        <Cell
                          key={index}
                          fill={COLORS[index]}
                        />
                      )
                    )}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>

          {/* =============================== */}
          {/* AI STATUS */}
          {/* =============================== */}
          <GlassCard title="AI Surveillance Status">
            <div className="space-y-4">
              <StatusItem
                label="Anomaly Engine"
                status="ACTIVE"
              />
              <StatusItem
                label="Forecasting Engine"
                status="RUNNING"
              />
              <StatusItem
                label="WHO Monitoring"
                status="CONNECTED"
              />
              <StatusItem
                label="Reddit Signals"
                status="LIVE"
              />
            </div>
          </GlassCard>

          {/* =============================== */}
          {/* REPORTS */}
          {/* =============================== */}
          <GlassCard title="Recent Reports">
            <div className="space-y-4">
              <ReportItem
                title="India Monthly Report"
              />
              <ReportItem
                title="Malawi Weekly Report"
              />
              <ReportItem
                title="Global AI Forecast"
              />
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}

/* ========================================== */
/* METRIC CARD */
/* ========================================== */
function MetricCard({
  title,
  value,
  icon,
  color,
}: MetricCardProps) {
  return (
    <motion.div
      whileHover={{
        y: -5,
      }}
      className="bg-white rounded-3xl shadow-xl p-6 border border-slate-100"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-500">
            {title}
          </p>
          <h2 className="text-4xl font-black mt-3">
            {value}
          </h2>
        </div>
        <div className={`${color} p-4 rounded-2xl text-white`}>
          {icon}
        </div>
      </div>
    </motion.div>
  );
}

/* ========================================== */
/* GLASS CARD */
/* ========================================== */
function GlassCard({
  title,
  children,
}: GlassCardProps) {
  return (
    <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-white/50 p-6">
      <h2 className="text-2xl font-bold text-slate-800 mb-6">
        {title}
      </h2>
      {children}
    </div>
  );
}

/* ========================================== */
/* FEED ITEM */
/* ========================================== */
function FeedItem({
  severity,
  disease,
  country,
}: FeedItemProps) {
  return (
    <div className="bg-slate-100 rounded-2xl p-4 flex items-center justify-between">
      <div>
        <h3 className="font-bold text-slate-800">
          {disease}
        </h3>
        <p className="text-slate-500">
          {country}
        </p>
      </div>
      <span className="bg-red-500 text-white px-4 py-2 rounded-xl text-sm font-semibold">
        {severity}
      </span>
    </div>
  );
}

/* ========================================== */
/* STATUS */
/* ========================================== */
function StatusItem({
  label,
  status,
}: StatusItemProps) {
  return (
    <div className="flex items-center justify-between bg-slate-100 rounded-2xl px-4 py-3">
      <span className="font-medium">
        {label}
      </span>
      <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm">
        {status}
      </span>
    </div>
  );
}

/* ========================================== */
/* REPORT ITEM */
/* ========================================== */
function ReportItem({
  title,
}: ReportItemProps) {
  return (
    <div className="flex items-center justify-between bg-slate-100 rounded-2xl px-4 py-3">
      <div className="flex items-center gap-3">
        <FileText className="text-blue-600" />
        <span className="font-medium">
          {title}
        </span>
      </div>
      <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm">
        View
      </button>
    </div>
  );
}
