import {
  Shield,
  Mail,
  Calendar,
  User,
  Trash2,
  Lock,
  Unlock,
  KeyRound,
} from "lucide-react"
import {
  sendResetEmail,
  disableUser as disableUserService,
  enableUser as enableUserService,
  deleteUser as deleteUserService,
} from "../../services/userService"

// =====================================================
// TYPES
// =====================================================

export interface AdminUser {

  id: number

  name: string

  email: string

  gender: string

  dob: string

  role: string

  is_active: boolean

  created_at?: string
}

interface Props {

  users: AdminUser[]

  loading: boolean

  refreshUsers: () => void
}

// =====================================================
// COMPONENT
// =====================================================

export default function UserTable({

  users,

  loading,

  refreshUsers,

}: Props) {

  // ===================================================
  // ACTIONS
  // ===================================================

  async function disableUser(
    id: number
  ) {

    try {

      await disableUserService(id)

      refreshUsers()

    } catch (error) {

      console.error(error)
    }
  }

  async function enableUser(
    id: number
  ) {

    try {

      await enableUserService(id)

      refreshUsers()

    } catch (error) {

      console.error(error)
    }
  }

  async function deleteUser(
    id: number
  ) {

    const confirmed =
      window.confirm(
        "Delete this user?"
      )

    if (!confirmed) return

    try {

      await deleteUserService(id)

      refreshUsers()

    } catch (error) {

      console.error(error)
    }
  }

  async function resetPassword(
    email: string
  ) {

    try {

      await sendResetEmail(email)

      alert(
        "Password reset email sent"
      )

    } catch (error) {

      console.error(error)
    }
  }

  // ===================================================
  // LOADING
  // ===================================================

  if (loading) {

    return (

      <div
        className="
          rounded-3xl
          border
          bg-white
          p-10
          text-center
          text-gray-500
        "
      >
        Loading users...
      </div>
    )
  }

  // ===================================================
  // EMPTY
  // ===================================================

  if (!users.length) {

    return (

      <div
        className="
          rounded-3xl
          border
          bg-white
          p-10
          text-center
        "
      >

        <div
          className="
            mx-auto
            flex
            h-16
            w-16
            items-center
            justify-center
            rounded-2xl
            bg-indigo-50
          "
        >

          <Shield
            size={28}
            className="text-indigo-600"
          />

        </div>

        <h3
          className="
            mt-5
            text-xl
            font-bold
            text-gray-800
          "
        >
          No Sub Admins Yet
        </h3>

        <p
          className="
            mt-2
            text-sm
            text-gray-500
          "
        >
          Create your first administrator
        </p>

      </div>
    )
  }

  // ===================================================
  // UI
  // ===================================================

  return (

    <div
      className="
        overflow-hidden
        rounded-3xl
        border
        bg-white
        shadow-sm
      "
    >

      {/* HEADER */}

      <div
        className="
          flex
          items-center
          justify-between
          border-b
          px-6
          py-5
        "
      >

        <div>

          <h2
            className="
              text-xl
              font-bold
              text-gray-800
            "
          >
            Platform Administrators
          </h2>

          <p
            className="
              mt-1
              text-sm
              text-gray-500
            "
          >
            Manage sub-admin access
          </p>

        </div>

        <div
          className="
            rounded-xl
            bg-indigo-50
            px-3
            py-2
            text-sm
            font-semibold
            text-indigo-700
          "
        >
          {users.length} Users
        </div>

      </div>

      {/* TABLE */}

      <div className="overflow-x-auto">

        <table className="min-w-full">

          <thead
            className="
              bg-gray-50
              text-left
            "
          >

            <tr>

              <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-gray-500">
                User
              </th>

              <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-gray-500">
                Gender
              </th>

              <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-gray-500">
                DOB
              </th>

              <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-gray-500">
                Role
              </th>

              <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-gray-500">
                Status
              </th>

              <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-gray-500">
                Actions
              </th>

            </tr>

          </thead>

          <tbody>

            {users.map((user) => (

              <tr
                key={user.id}
                className="
                  border-t
                  hover:bg-gray-50
                "
              >

                {/* USER */}

                <td className="px-6 py-5">

                  <div
                    className="
                      flex
                      items-center
                      gap-4
                    "
                  >

                    <div
                      className="
                        flex
                        h-12
                        w-12
                        items-center
                        justify-center
                        rounded-2xl
                        bg-indigo-100
                      "
                    >

                      <User
                        size={20}
                        className="text-indigo-600"
                      />

                    </div>

                    <div>

                      <h3
                        className="
                          font-semibold
                          text-gray-800
                        "
                      >
                        {user.name}
                      </h3>

                      <div
                        className="
                          mt-1
                          flex
                          items-center
                          gap-2
                          text-sm
                          text-gray-500
                        "
                      >

                        <Mail size={14} />

                        {user.email}

                      </div>

                    </div>

                  </div>

                </td>

                {/* GENDER */}

                <td className="px-6 py-5 text-sm text-gray-700">
                  {user.gender}
                </td>

                {/* DOB */}

                <td className="px-6 py-5">

                  <div
                    className="
                      flex
                      items-center
                      gap-2
                      text-sm
                      text-gray-700
                    "
                  >

                    <Calendar size={14} />

                    {user.dob}

                  </div>

                </td>

                {/* ROLE */}

                <td className="px-6 py-5">

                  <div
                    className="
                      inline-flex
                      rounded-full
                      bg-indigo-100
                      px-3
                      py-1
                      text-xs
                      font-semibold
                      text-indigo-700
                    "
                  >
                    {user.role}
                  </div>

                </td>

                {/* STATUS */}

                <td className="px-6 py-5">

                  <div
                    className={`
                      inline-flex
                      rounded-full
                      px-3
                      py-1
                      text-xs
                      font-semibold

                      ${
                        user.is_active

                        ? "bg-green-100 text-green-700"

                        : "bg-red-100 text-red-700"
                      }
                    `}
                  >

                    {user.is_active
                      ? "Active"
                      : "Disabled"
                    }

                  </div>

                </td>

                {/* ACTIONS */}

                <td className="px-6 py-5">

                  <div
                    className="
                      flex
                      flex-wrap
                      gap-2
                    "
                  >

                    {/* RESET */}

                    <button
                      onClick={() =>
                        resetPassword(
                          user.email
                        )
                      }
                      className="
                        inline-flex
                        items-center
                        gap-1
                        rounded-lg
                        bg-blue-100
                        px-3
                        py-2
                        text-xs
                        font-medium
                        text-blue-700
                        hover:bg-blue-200
                      "
                    >

                      <KeyRound size={14} />

                      Reset

                    </button>

                    {/* DISABLE / ENABLE */}

                    {user.is_active ? (

                      <button
                        onClick={() =>
                          disableUser(
                            user.id
                          )
                        }
                        className="
                          inline-flex
                          items-center
                          gap-1
                          rounded-lg
                          bg-yellow-100
                          px-3
                          py-2
                          text-xs
                          font-medium
                          text-yellow-700
                          hover:bg-yellow-200
                        "
                      >

                        <Lock size={14} />

                        Disable

                      </button>

                    ) : (

                      <button
                        onClick={() =>
                          enableUser(
                            user.id
                          )
                        }
                        className="
                          inline-flex
                          items-center
                          gap-1
                          rounded-lg
                          bg-green-100
                          px-3
                          py-2
                          text-xs
                          font-medium
                          text-green-700
                          hover:bg-green-200
                        "
                      >

                        <Unlock size={14} />

                        Enable

                      </button>

                    )}

                    {/* DELETE */}

                    <button
                      onClick={() =>
                        deleteUser(
                          user.id
                        )
                      }
                      className="
                        inline-flex
                        items-center
                        gap-1
                        rounded-lg
                        bg-red-100
                        px-3
                        py-2
                        text-xs
                        font-medium
                        text-red-700
                        hover:bg-red-200
                      "
                    >

                      <Trash2 size={14} />

                      Delete

                    </button>

                  </div>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  )
}
