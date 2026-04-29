"use client"

import { signOut } from "firebase/auth"
import { auth } from "../../firebase"

// 🔹 Props type
interface HeaderProps {
  title?: string
}

export default function Header({ title }: HeaderProps) {
  return (
    <header className="h-16 bg-white border-b flex items-center justify-between px-8">

      {/* 🔹 LEFT: Dynamic Title */}
      <div className="flex flex-col">
        <span className="text-slate-800 font-semibold text-sm">
          {title || "Infodemiology Dashboard"}
        </span>
        <span className="text-xs text-slate-500">
          Early Warning System
        </span>
      </div>

      {/* 🔹 RIGHT: User + Logout */}
      <div className="flex items-center gap-4">

        <div className="text-sm text-slate-600">
          Dr. A. Sharma
        </div>

        <img
          src="https://i.pravatar.cc/40"
          alt="User"
          className="w-8 h-8 rounded-full border"
        />

        <button
          onClick={() => signOut(auth)}
          className="text-sm text-red-600 hover:underline"
        >
          Logout
        </button>

      </div>
    </header>
  )
}