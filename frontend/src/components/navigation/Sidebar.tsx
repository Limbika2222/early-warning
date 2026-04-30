"use client"

import { NavLink } from "react-router-dom"
import { motion } from "framer-motion"
import {
  LayoutDashboard,
  Upload,
  Activity,
  AlertTriangle,
  FileText,
  Settings,
  BookOpen,
  Globe,
  MessageCircle,
} from "lucide-react"

// -------------------------------------------------
// MENU
// -------------------------------------------------
const menu = [
  { label: "Google Dashboard", icon: LayoutDashboard, path: "/" },
  { label: "Reddit Signals", icon: MessageCircle, path: "/reddit" },
  { label: "WHO Surveillance", icon: Globe, path: "/who" },
  { label: "Upload Data", icon: Upload, path: "/upload" },
  { label: "Predictions", icon: Activity, path: "/predictions" },
  { label: "Alerts & Anomalies", icon: AlertTriangle, path: "/alerts" },
  { label: "Reports", icon: FileText, path: "/reports" },
  { label: "Settings", icon: Settings, path: "/settings" },
  { label: "Documentation", icon: BookOpen, path: "/docs" },
]

// -------------------------------------------------
// COMPONENT
// -------------------------------------------------
export default function Sidebar() {
  return (
    <aside
      className="
        w-[260px]
        bg-slate-900
        text-slate-200
        border-r border-slate-800
        flex flex-col
      "
    >
      {/* 🔹 Logo */}
      <div className="px-8 py-6 border-b border-slate-800">
        <h1 className="text-lg font-semibold text-white tracking-wide">
          Infodemiology
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Early Warning System
        </p>
      </div>

      {/* 🔹 Navigation */}
      <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
        {menu.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.label}
              to={item.path}
              end={item.path === "/"}
            >
              {({ isActive }) => (
                <motion.div
                  whileHover={{ x: 4 }}
                  transition={{ type: "spring", stiffness: 260 }}
                  className={`
                    relative flex items-center gap-3 px-4 py-2.5 rounded-lg
                    text-sm font-medium transition-all duration-200
                    ${
                      isActive
                        ? "bg-indigo-600 text-white"
                        : "text-slate-400 hover:bg-slate-800 hover:text-white"
                    }
                  `}
                >
                  {/* Active indicator */}
                  {isActive && (
                    <motion.div
                      layoutId="activeSidebarIndicator"
                      className="absolute left-0 top-0 bottom-0 w-1 bg-indigo-400 rounded-r-full"
                    />
                  )}

                  {/* Icon */}
                  <Icon
                    size={18}
                    className={`transition-all duration-200 ${
                      isActive ? "text-white" : "text-slate-400"
                    }`}
                  />

                  {/* Label */}
                  <span>{item.label}</span>
                </motion.div>
              )}
            </NavLink>
          )
        })}
      </nav>

      {/* 🔹 Footer */}
      <div className="px-6 py-5 border-t border-slate-800 text-xs text-slate-500">
        Limbika–Shonith IIC · v1.0 · 2026
      </div>
    </aside>
  )
}