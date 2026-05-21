"use client"

import { NavLink } from "react-router-dom"
import { motion } from "framer-motion"

import {
  LayoutDashboard,
  Upload,
  AlertTriangle,
  FileText,
  Settings,
  BookOpen,
  Globe,
  MessageCircle,
  Brain,
} from "lucide-react"

// =====================================================
// MENU
// =====================================================

const menu = [

  // ===================================================
  // MAIN AI MODULE
  // ===================================================

  {
    section: "AI Intelligence",

    items: [

      {
        label: "Predictions Dashboard",
        icon: Brain,
        path: "/predictions",
      },

      {
        label: "WHO Surveillance",
        icon: Globe,
        path: "/who",
      },

      {
        label: "Google Trends",
        icon: LayoutDashboard,
        path: "/",
      },

      {
        label: "Upload Trends Data",
        icon: Upload,
        path: "/upload",
      },

      {
        label: "Reddit Signals",
        icon: MessageCircle,
        path: "/reddit",
      },
    ],
  },

  // ===================================================
  // ANALYTICS
  // ===================================================

  {
    section: "Analytics",

    items: [

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
    ],
  },

  // ===================================================
  // SYSTEM
  // ===================================================

  {
    section: "System",

    items: [

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
    ],
  },
]

// =====================================================
// COMPONENT
// =====================================================

export default function Sidebar() {

  return (

    <aside
      className="
        w-[270px]
        bg-slate-900
        text-slate-200
        border-r border-slate-800
        flex flex-col
      "
    >

      {/* =================================================
          LOGO
      ================================================= */}

      <div
        className="
          px-8 py-6
          border-b border-slate-800
        "
      >

        <h1
          className="
            text-xl
            font-bold
            text-white
            tracking-wide
          "
        >
          Infodemiology
        </h1>

        <p
          className="
            text-xs
            text-slate-400
            mt-1
          "
        >
          AI Early Warning System
        </p>

      </div>

      {/* =================================================
          NAVIGATION
      ================================================= */}

      <nav
        className="
          flex-1
          px-3 py-6
          overflow-y-auto
        "
      >

        {menu.map((group) => (

          <div
            key={group.section}
            className="mb-8"
          >

            {/* SECTION TITLE */}

            <p
              className="
                px-3 mb-3
                text-[11px]
                uppercase
                tracking-[0.2em]
                text-slate-500
                font-semibold
              "
            >
              {group.section}
            </p>

            {/* MENU ITEMS */}

            <div className="space-y-1">

              {group.items.map((item) => {

                const Icon = item.icon

                return (

                  <NavLink
                    key={item.label}
                    to={item.path}
                    end={item.path === "/"}
                  >

                    {({ isActive }) => (

                      <motion.div

                        whileHover={{
                          x: 4,
                        }}

                        transition={{
                          type: "spring",
                          stiffness: 260,
                        }}

                        className={`
                          relative
                          flex items-center
                          gap-3
                          px-4 py-3
                          rounded-xl
                          text-sm
                          font-medium
                          transition-all
                          duration-200

                          ${
                            isActive
                              ? "bg-indigo-600 text-white shadow-lg"
                              : "text-slate-400 hover:bg-slate-800 hover:text-white"
                          }
                        `}
                      >

                        {/* ACTIVE INDICATOR */}

                        {isActive && (

                          <motion.div
                            layoutId="activeSidebarIndicator"

                            className="
                              absolute
                              left-0
                              top-0
                              bottom-0
                              w-1
                              bg-indigo-300
                              rounded-r-full
                            "
                          />

                        )}

                        {/* ICON */}

                        <Icon
                          size={18}

                          className={
                            isActive
                              ? "text-white"
                              : "text-slate-400"
                          }
                        />

                        {/* LABEL */}

                        <span>
                          {item.label}
                        </span>

                      </motion.div>

                    )}

                  </NavLink>

                )
              })}

            </div>

          </div>

        ))}

      </nav>

      {/* =================================================
          FOOTER
      ================================================= */}

      <div
        className="
          px-6 py-5
          border-t border-slate-800
          text-xs
          text-slate-500
        "
      >

        Limbika–Shonith IIC · v1.0 · 2026

      </div>

    </aside>
  )
}