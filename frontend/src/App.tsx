import { useEffect, useState } from "react"
import { HashRouter, Routes, Route, Navigate } from "react-router-dom"
import { onAuthStateChanged } from "firebase/auth"
import type { User } from "firebase/auth"

import { auth } from "./firebase"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import UploadData from "./pages/UploadData"

export default function App() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, currentUser => {
      setUser(currentUser)
      setLoading(false)
    })

    return unsubscribe
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen text-gray-500">
        Loading application…
      </div>
    )
  }

  return (
    <HashRouter>
      <Routes>
        {/* Public */}
        <Route
          path="/login"
          element={user ? <Navigate to="/" /> : <Login />}
        />

        {/* Protected */}
        <Route
          path="/"
          element={user ? <Dashboard /> : <Navigate to="/login" />}
        />

        <Route
          path="/upload"
          element={user ? <UploadData /> : <Navigate to="/login" />}
        />

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </HashRouter>
  )
}
