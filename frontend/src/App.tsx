import { useEffect, useState } from "react"
import { HashRouter, Routes, Route, Navigate } from "react-router-dom"
import { onAuthStateChanged } from "firebase/auth"
import type { User } from "firebase/auth"

import { auth } from "./firebase"
import { DashboardProvider } from "./context/DashboardContext"

import AppLayout from "./components/layout/AppLayout"
import Login from "./pages/Login"
import UploadData from "./pages/UploadData"
import NewDashboard from "./pages/NewDashboard"

export default function App() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser)
      setLoading(false)
    })
    return unsub
  }, [])

  // 🔄 Loading Screen
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700">
        <div className="text-center">
          <div className="animate-pulse text-white text-2xl font-semibold">
            Infodemiology Intelligence Platform
          </div>
          <p className="text-blue-100 mt-2 text-sm">
            Initializing Early Warning System…
          </p>
        </div>
      </div>
    )
  }

  return (
    <HashRouter>
      <Routes>
        {/* Public Route */}
        <Route
          path="/login"
          element={user ? <Navigate to="/" /> : <Login />}
        />

        {/* Protected Layout */}
        <Route
          element={user ? <AppLayout /> : <Navigate to="/login" />}
        >
          <Route
            path="/"
            element={
              <DashboardProvider>
                <NewDashboard />
              </DashboardProvider>
            }
          />
          <Route path="/upload" element={<UploadData />} />
        </Route>

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </HashRouter>
  )
}