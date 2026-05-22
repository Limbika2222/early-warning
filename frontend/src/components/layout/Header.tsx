"use client"

import { signOut } from "firebase/auth"

import { auth } from "../../firebase"

import {
  useEffect,
  useState,
} from "react"

// =====================================================
// TYPES
// =====================================================

interface HeaderProps {

  title?: string
}

// =====================================================
// COMPONENT
// =====================================================

export default function Header({

  title,

}: HeaderProps) {

  // ===================================================
  // STATE
  // ===================================================

  const [userName, setUserName] =
    useState("Administrator")

  const [userEmail, setUserEmail] =
    useState("")

  const [photoURL, setPhotoURL] =
    useState("")

  // ===================================================
  // LOAD AUTH USER
  // ===================================================

  useEffect(() => {

    const unsubscribe =
      auth.onAuthStateChanged(

        (user) => {

          if (user) {

            setUserName(

              user.displayName ||

              "Administrator"
            )

            setUserEmail(

              user.email || ""
            )

            setPhotoURL(

              user.photoURL || ""
            )
          }
        }
      )

    return () =>
      unsubscribe()

  }, [])

  // ===================================================
  // LOGOUT
  // ===================================================

  async function handleLogout() {

    try {

      await signOut(auth)

    } catch (error) {

      console.error(
        "Logout Error:",
        error
      )
    }
  }

  // ===================================================
  // UI
  // ===================================================

  return (

    <header
      className="
        h-16
        bg-white
        border-b
        flex
        items-center
        justify-between
        px-8
      "
    >

      {/* LEFT */}

      <div
        className="
          flex
          flex-col
        "
      >

        <span
          className="
            text-slate-800
            font-semibold
            text-sm
          "
        >
          {title ||
            "Infodemiology Dashboard"}
        </span>

        <span
          className="
            text-xs
            text-slate-500
          "
        >
          Early Warning System
        </span>

      </div>

      {/* RIGHT */}

      <div
        className="
          flex
          items-center
          gap-4
        "
      >

        {/* USER INFO */}

        <div
          className="
            flex
            flex-col
            text-right
          "
        >

          <span
            className="
              text-sm
              font-medium
              text-slate-700
            "
          >
            {userName}
          </span>

          <span
            className="
              text-xs
              text-slate-500
            "
          >
            {userEmail}
          </span>

        </div>

        {/* AVATAR */}

        {photoURL ? (

          <img
            src={photoURL}
            alt="User"
            className="
              w-9
              h-9
              rounded-full
              border
              object-cover
            "
          />

        ) : (

          <div
            className="
              w-9
              h-9
              rounded-full
              bg-indigo-100
              flex
              items-center
              justify-center
              text-indigo-700
              font-semibold
            "
          >

            {userName.charAt(0)}

          </div>
        )}

        {/* LOGOUT */}

        <button
          onClick={handleLogout}
          className="
            text-sm
            text-red-600
            hover:underline
          "
        >
          Logout
        </button>

      </div>

    </header>
  )
}