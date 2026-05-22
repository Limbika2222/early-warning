import { useEffect, useState } from "react"
import { Shield, UserPlus } from "lucide-react"
import AddUserModal from "../components/settings/AddUserModal"
import UserTable, { type AdminUser } from "../components/settings/UserTable"
import { getUsers } from "../services/userService"

// =====================================================
// COMPONENT
// =====================================================

export default function Settings() {
  // ===================================================
  // STATE
  // ===================================================

  const [openModal, setOpenModal] = useState(false)
  const [loading, setLoading] = useState(true)
  const [users, setUsers] = useState<AdminUser[]>([])

  // ===================================================
  // FETCH USERS
  // ===================================================

  async function refreshUsers() {
    try {
      setLoading(true)
      const fetchedUsers = await getUsers()
      setUsers(fetchedUsers)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  // ===================================================
  // LOAD USERS
  // ===================================================

  useEffect(() => {
    refreshUsers()
  }, [])

  // ===================================================
  // AFTER CREATE USER
  // ===================================================

  function handleSuccess() {
    refreshUsers()
    setOpenModal(false)
  }

  // ===================================================
  // UI
  // ===================================================

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      {/* HEADER */}
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <div className="flex items-center gap-3">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-100">
              <Shield size={28} className="text-indigo-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Settings</h1>
              <p className="mt-1 text-sm text-gray-500">
                User & access management
              </p>
            </div>
          </div>
        </div>
        {/* ADD BUTTON */}
        <button
          onClick={() => setOpenModal(true)}
          className="inline-flex items-center gap-2 rounded-2xl bg-indigo-600 px-5 py-3 font-semibold text-white shadow-lg transition-all hover:bg-indigo-700"
        >
          <UserPlus size={18} />
          Add Sub Admin
        </button>
      </div>

      {/* USER TABLE */}
      <UserTable users={users} loading={loading} refreshUsers={refreshUsers} />

      {/* MODAL */}
      <AddUserModal
        open={openModal}
        onClose={() => setOpenModal(false)}
        onSuccess={handleSuccess}
      />
    </div>
  )
}
