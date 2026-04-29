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
// ✅ FIXED MENU (MATCHES App.tsx EXACTLY)
// -------------------------------------------------
const menu = [
  { label: "Google Dashboard", icon: LayoutDashboard, path: "/" },

  // 🔥 FIXED (must match App.tsx)
  { label: "Reddit Signals", icon: MessageCircle, path: "/reddit" },
  { label: "WHO Surveillance", icon: Globe, path: "/who" },

  { label: "Upload Data", icon: Upload, path: "/upload" },

  // Optional sections
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
        bg-white/30
        backdrop-blur-xl
        border-r border-white/40
        flex flex-col
        shadow-lg
      "
    >
      {/* 🔹 Logo */}
      <div className="px-8 py-6 border-b border-white/40">
        <h1 className="text-xl font-semibold text-[#1e3f42] tracking-wide">
          Infodemiology
        </h1>
        <p className="text-xs text-[#3b6b6f] mt-1">
          Early Warning System
        </p>
      </div>

      {/* 🔹 Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        {menu.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.label}
              to={item.path}
              end={item.path === "/"} // exact match for root
            >
              {({ isActive }) => (
                <motion.div
                  whileHover={{ x: 6 }}
                  transition={{ type: "spring", stiffness: 300 }}
                  className={`
                    relative flex items-center gap-3 px-4 py-3 rounded-xl
                    text-sm font-medium transition-all duration-300
                    ${
                      isActive
                        ? "bg-white/80 text-[#1f9c94] shadow-md"
                        : "text-[#1e3f42] hover:bg-white/50"
                    }
                  `}
                >
                  {/* Active indicator */}
                  {isActive && (
                    <motion.div
                      layoutId="activeSidebarIndicator"
                      className="absolute left-0 top-0 bottom-0 w-1 bg-[#1f9c94] rounded-r-full"
                    />
                  )}

                  {/* Icon */}
                  <Icon
                    size={18}
                    className={`transition-transform duration-200 ${
                      isActive ? "scale-110 text-[#1f9c94]" : ""
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
      <div className="px-6 py-5 border-t border-white/40 text-xs text-[#3b6b6f]">
        Limbika–Shonith IIC · v1.0 · 2026
      </div>
    </aside>
  )
}