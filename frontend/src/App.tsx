"use client"

import {
  HashRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom"

import {
  useState,
} from "react"

import { DashboardProvider } from "./context/DashboardContext"

import AppLayout from "./components/layout/AppLayout"

import Login from "./pages/Login"

import UploadData from "./pages/UploadData"

import NewDashboard from "./pages/NewDashboard"

import WhoDashboard from "./pages/WhoDashboard"

import RedditDashboard from "./pages/RedditDashboard"

import PredictionsDashboard from "./pages/PredictionsDashboard"

import Settings from "./pages/Settings"

import Alerts from "./pages/Alerts"

import Reports from "./pages/Reports"

export default function App() {

  // ===================================================
  // AUTH STATE
  // ===================================================

  const [authenticated,
    setAuthenticated] =
    useState(

      !!localStorage.getItem(
        "token"
      )
    )

  // ===================================================
  // LOGIN SUCCESS
  // ===================================================

  function handleLoginSuccess() {

    setAuthenticated(true)
  }

  // ===================================================
  // ROUTES
  // ===================================================

  return (

    <HashRouter>

      <Routes>

        {/* ---------------- LOGIN ---------------- */}

        <Route
          path="/login"
          element={
            authenticated
              ? <Navigate to="/" />
              : (
                <Login
                  onLoginSuccess={
                    handleLoginSuccess
                  }
                />
              )
          }
        />

        {/* ---------------- PROTECTED ---------------- */}

        <Route
          element={
            authenticated
              ? <AppLayout />
              : <Navigate to="/login" />
          }
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

          <Route
            path="/upload"
            element={<UploadData />}
          />

          {/* ⚙️ SETTINGS */}

          <Route
            path="/settings"
            element={<Settings />}
          />

          {/* ⚠️ ALERTS */}

          <Route
            path="/alerts"
            element={
              <DashboardProvider>
                <Alerts />
              </DashboardProvider>
            }
          />

          {/* 📄 REPORTS */}

          <Route
            path="/reports"
            element={<Reports />}
          />

        </Route>

        {/* ---------------- FALLBACK ---------------- */}

        <Route
          path="*"
          element={<Navigate to="/" />}
        />

      </Routes>

    </HashRouter>
  )
}