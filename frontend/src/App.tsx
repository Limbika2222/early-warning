import { useEffect, useState } from "react"
import { onAuthStateChanged } from "firebase/auth"
import type { User } from "firebase/auth"

import { auth } from "./firebase"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"

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
    return <div className="p-6">Loading...</div>
  }

  return user ? <Dashboard /> : <Login />
}
