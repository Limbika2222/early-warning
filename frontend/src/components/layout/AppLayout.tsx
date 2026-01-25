import { Outlet } from "react-router-dom"
import Sidebar from "../navigation/Sidebar"
import Header from "./Header"

export default function AppLayout() {
  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar always visible */}
      <Sidebar />

      <div className="flex flex-col flex-1">
        <Header />

        {/* Page content switches here */}
        <main className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
