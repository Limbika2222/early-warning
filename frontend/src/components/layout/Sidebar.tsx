import { NavLink } from "react-router-dom"
import { motion } from "framer-motion"
import {
  LayoutDashboard,
  Upload,
  Activity,
  AlertTriangle,
  Settings,
  Globe,
  MessageCircle
} from "lucide-react"

const menu = [
  { label: "Dashboard", icon: LayoutDashboard, path: "/" },
  { label: "Reddit Signals", icon: MessageCircle, path: "/reddit" },
  { label: "WHO Data", icon: Globe, path: "/who" },
  { label: "Upload Data", icon: Upload, path: "/upload" },
  { label: "Predictions", icon: Activity, path: "/predictions" },
  { label: "Alerts", icon: AlertTriangle, path: "/alerts" },
  { label: "Settings", icon: Settings, path: "/settings" },
]

export default function Sidebar() {
  return (
    <aside
      className="
        w-[250px]
        bg-white/30
        backdrop-blur-xl
        border-r border-white/40
        flex flex-col
        shadow-lg
      "
    >
      {/* Logo Section */}
      <div className="px-8 py-6 border-b border-white/40">
        <h1 className="text-xl font-semibold text-[#1e3f42] tracking-wide">
          Infodemiology
        </h1>
        <p className="text-xs text-[#3b6b6f] mt-1">
          Early Warning System
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {menu.map((item) => {
          const Icon = item.icon

          return (
            <NavLink key={item.label} to={item.path}>
              {({ isActive }) => (
                <motion.div
                  whileHover={{ x: 6 }}
                  transition={{ type: "spring", stiffness: 300 }}
                  className={`
                    relative flex items-center gap-3 px-4 py-3 rounded-xl
                    text-sm font-medium transition-all duration-300
                    ${
                      isActive
                        ? "bg-white/70 text-[#1f9c94] shadow-md"
                        : "text-[#1e3f42] hover:bg-white/50"
                    }
                  `}
                >
                  {/* Active accent bar */}
                  {isActive && (
                    <motion.div
                      layoutId="activeSidebarIndicator"
                      className="absolute left-0 top-0 bottom-0 w-1 bg-[#1f9c94] rounded-r-full"
                    />
                  )}

                  <Icon
                    size={18}
                    className={`transition-transform duration-200 ${
                      isActive ? "scale-110 text-[#1f9c94]" : ""
                    }`}
                  />

                  <span>{item.label}</span>
                </motion.div>
              )}
            </NavLink>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="px-6 py-5 border-t border-white/40 text-xs text-[#3b6b6f]">
        Limbika-Shonith-IIC · v1.0 · 2026
      </div>
    </aside>
  )
}