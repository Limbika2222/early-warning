import { signOut } from "firebase/auth"
import { auth } from "../../firebase"

export default function Header() {
  return (
    <header className="h-16 bg-white border-b flex items-center justify-between px-8">
      <div className="text-slate-800 font-semibold">
        Infodemiology Early Warning System
      </div>

      <div className="flex items-center gap-4">
        <div className="text-sm text-slate-600">
          Dr. A. Sharma
        </div>
        <img
          src="https://i.pravatar.cc/40"
          className="w-8 h-8 rounded-full"
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
