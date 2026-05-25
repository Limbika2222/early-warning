import { useState } from "react"

import { loginUser } from "../api/auth"

// =====================================================
// TYPES
// =====================================================

interface LoginProps {

  onLoginSuccess: () => void
}

// =====================================================
// COMPONENT
// =====================================================

export default function Login({

  onLoginSuccess,

}: LoginProps) {

  const [email, setEmail] =
    useState("")

  const [password, setPassword] =
    useState("")

  const [error, setError] =
    useState("")

  const [loading, setLoading] =
    useState(false)

  // ===================================================
  // LOGIN
  // ===================================================

  async function handleLogin(
    e: React.FormEvent
  ) {

    e.preventDefault()

    try {

      setLoading(true)

      setError("")

      const result =
        await loginUser(

          email,

          password
        )

      // ===============================================
      // SAVE TOKEN
      // ===============================================

      localStorage.setItem(

        "token",

        result.access_token
      )

      localStorage.setItem(

        "user",

        JSON.stringify(
          result.user
        )
      )

      console.log(
        "✅ Login success"
      )

      // ===============================================
      // UPDATE APP STATE
      // ===============================================

      onLoginSuccess()

    } catch (err: unknown) {

      console.error(
        "❌ Login error:",
        err
      )

      if (err instanceof Error) {

        setError(err.message)

      } else {

        setError(
          "Login failed"
        )
      }

    } finally {

      setLoading(false)
    }
  }

  // ===================================================
  // UI
  // ===================================================

  return (

    <div
      className="
        min-h-screen
        flex
        items-center
        justify-center
        bg-gray-100
      "
    >

      <form
        onSubmit={handleLogin}
        className="
          bg-white
          p-8
          rounded-xl
          shadow-md
          w-full
          max-w-md
        "
      >

        <h1
          className="
            text-3xl
            font-bold
            mb-6
            text-center
          "
        >
          Early Warning Dashboard
        </h1>

        {error && (

          <div
            className="
              mb-4
              text-red-500
              text-sm
            "
          >
            {error}
          </div>
        )}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(
              e.target.value
            )
          }
          className="
            w-full
            border
            p-3
            rounded-lg
            mb-4
          "
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(
              e.target.value
            )
          }
          className="
            w-full
            border
            p-3
            rounded-lg
            mb-6
          "
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="
            w-full
            bg-blue-600
            hover:bg-blue-700
            text-white
            p-3
            rounded-lg
            disabled:opacity-50
          "
        >

          {loading
            ? "Signing in..."
            : "Sign In"}

        </button>

      </form>

    </div>
  )
}