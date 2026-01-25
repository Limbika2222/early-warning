import { NavLink } from "react-router-dom"
import {
  LayoutDashboard,
  Upload,
  Activity,
  AlertTriangle,
  FileText,
  Settings,
  BookOpen,
} from "lucide-react"

const menu = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/",
  },
  {
    label: "Upload Data",
    icon: Upload,
    path: "/upload",
  },
  {
    label: "Predictions",
    icon: Activity,
    path: "/predictions",
  },
  {
    label: "Alerts & Anomalies",
    icon: AlertTriangle,
    path: "/alerts",
  },
  {
    label: "Reports",
    icon: FileText,
    path: "/reports",
  },
  {
    label: "Settings",
    icon: Settings,
    path: "/settings",
  },
  {
    label: "Documentation",
    icon: BookOpen,
    path: "/docs",
  },
]

export default function Sidebar() {
  return (
    <aside className="w-[280px] bg-slate-900 text-slate-100 flex flex-col">
      {/* Logo / Title */}
      <div className="px-6 py-5 text-lg font-semibold tracking-wide border-b border-slate-800">
        Infodemiology EWS
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {menu.map(item => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.label}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-md text-sm transition
                 ${
                   isActive
                     ? "bg-slate-800 text-blue-400"
                     : "text-slate-300 hover:bg-slate-800/60 hover:text-slate-100"
                 }`
              }
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 text-xs text-slate-400 border-t border-slate-800">
        Limbika-IIC · v1.0 · 2026
      </div>
    </aside>
  )
}
