import { Outlet } from "react-router-dom"
import Sidebar from "../navigation/Sidebar"
import Header from "./Header"

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#9bd5d1] via-[#8cced0] to-[#b5e3dc] p-6">

      {/* Glass container */}
      <div className="h-full rounded-[32px] bg-white/40 backdrop-blur-xl border border-white/40 shadow-2xl overflow-hidden flex">

        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <div className="flex flex-col flex-1 overflow-hidden">

          <Header />

          <main className="flex-1 overflow-y-auto p-10">
            <div className="max-w-7xl mx-auto">
              <Outlet />
            </div>
          </main>

        </div>
      </div>
    </div>
  )
}
