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
  { label: "Dashboard", icon: LayoutDashboard, active: true },
  { label: "Upload Data", icon: Upload },
  { label: "Predictions", icon: Activity },
  { label: "Alerts & Anomalies", icon: AlertTriangle },
  { label: "Reports", icon: FileText },
  { label: "Settings", icon: Settings },
  { label: "Documentation", icon: BookOpen },
]

export default function Sidebar() {
  return (
    <aside className="w-[280px] bg-slate-900 text-slate-100 flex flex-col">
      <div className="px-6 py-5 text-lg font-semibold tracking-wide">
        Infodemiology EWS
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {menu.map(item => (
          <div
            key={item.label}
            className={`flex items-center gap-3 px-4 py-3 rounded-md cursor-pointer
              ${item.active
                ? "bg-slate-800 text-blue-400"
                : "hover:bg-slate-800/60"}`}
          >
            <item.icon size={18} />
            <span className="text-sm">{item.label}</span>
          </div>
        ))}
      </nav>

      <div className="px-4 py-4 text-xs text-slate-400 border-t border-slate-800">
        Limbika-iic – 2026
      </div>
    </aside>
  )
}
