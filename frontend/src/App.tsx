"use client"

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
import WhoDashboard from "./pages/WhoDashboard"
import RedditDashboard from "./pages/RedditDashboard"
import PredictionsDashboard from "./pages/PredictionsDashboard"
import Settings from "./pages/Settings"

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

        {/* ---------------- PUBLIC ---------------- */}
        <Route
          path="/login"
          element={user ? <Navigate to="/" /> : <Login />}
        />

        {/* ---------------- PROTECTED ---------------- */}
        <Route
          element={user ? <AppLayout /> : <Navigate to="/login" />}
        >

          {/* 🟢 GOOGLE */}
          <Route
            path="/"
            element={
              <DashboardProvider>
                <NewDashboard />
              </DashboardProvider>
            }
          />

          {/* 🔵 REDDIT */}
          <Route
            path="/reddit"
            element={
              <DashboardProvider>
                <RedditDashboard />
              </DashboardProvider>
            }
          />

          {/* 🟣 WHO */}
          <Route
            path="/who"
            element={
              <DashboardProvider>
                <WhoDashboard />
              </DashboardProvider>
            }
          />
          
          {/* 📈 PREDICTIONS */}
          <Route
            path="/predictions"
            element={
              <DashboardProvider>
                <PredictionsDashboard />
              </DashboardProvider>
            }
          />

          {/* 📤 UPLOAD */}
          <Route path="/upload" element={<UploadData />} />
          
          {/* ⚙️ SETTINGS */}
          <Route path="/settings" element={<Settings />} />

        </Route>

        {/* ---------------- FALLBACK ---------------- */}
        <Route path="*" element={<Navigate to="/" />} />

      </Routes>
    </HashRouter>
  )
}