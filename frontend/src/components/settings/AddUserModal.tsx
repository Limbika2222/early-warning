import { useState } from "react"

import {
  X,
  Loader2,
  UserPlus,
} from "lucide-react"

import {
  createSubAdmin,
} from "../../services/userService"

// =====================================================
// TYPES
// =====================================================

interface Props {

  open: boolean

  onClose: () => void

  onSuccess: () => void
}

// =====================================================
// COMPONENT
// =====================================================

export default function AddUserModal({

  open,

  onClose,

  onSuccess,

}: Props) {

  // ===================================================
  // STATE
  // ===================================================

  const [name, setName] =
    useState("")

  const [email, setEmail] =
    useState("")

  const [gender, setGender] =
    useState("Male")

  const [dob, setDob] =
    useState("")

  const [loading, setLoading] =
    useState(false)

  const [error, setError] =
    useState("")

  const [success, setSuccess] =
    useState("")

  // ===================================================
  // SUBMIT
  // ===================================================

  async function handleSubmit() {

    try {

      setLoading(true)

      setError("")

      setSuccess("")

      await createSubAdmin({

        name,

        email,

        gender,

        dob,
      })

      setSuccess(
        "Sub-admin created successfully"
      )

      setTimeout(() => {

        onSuccess()

        onClose()

      }, 1200)

    } catch (err: unknown) {

      if (err instanceof Error) {

        setError(err.message)

      } else {

        setError(
          "Failed to create user"
        )
      }

    } finally {

      setLoading(false)
    }
  }

  // ===================================================
  // HIDE
  // ===================================================

  if (!open) return null

  // ===================================================
  // UI
  // ===================================================

  return (

    <div
      className="
        fixed
        inset-0
        z-50
        flex
        items-center
        justify-center
        bg-black/40
        backdrop-blur-sm
        p-4
      "
    >

      <div
        className="
          w-full
          max-w-lg
          rounded-3xl
          bg-white
          shadow-2xl
          overflow-hidden
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
                text-2xl
                font-bold
                text-gray-800
              "
            >
              Create Sub Admin
            </h2>

            <p
              className="
                text-sm
                text-gray-500
                mt-1
              "
            >
              Add a new platform administrator
            </p>

          </div>

          <button
            onClick={onClose}
            className="
              p-2
              rounded-xl
              hover:bg-gray-100
            "
          >

            <X size={20} />

          </button>

        </div>

        {/* BODY */}

        <div
          className="
            p-6
            space-y-5
          "
        >

          {/* NAME */}

          <div>

            <label
              className="
                text-sm
                font-medium
                text-gray-700
              "
            >
              Full Name
            </label>

            <input
              type="text"
              value={name}
              onChange={(e) =>
                setName(
                  e.target.value
                )
              }
              className="
                mt-2
                w-full
                rounded-xl
                border
                px-4
                py-3
                outline-none
                focus:ring-2
                focus:ring-indigo-500
              "
              placeholder="John Doe"
            />

          </div>

          {/* EMAIL */}

          <div>

            <label
              className="
                text-sm
                font-medium
                text-gray-700
              "
            >
              Email Address
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) =>
                setEmail(
                  e.target.value
                )
              }
              className="
                mt-2
                w-full
                rounded-xl
                border
                px-4
                py-3
                outline-none
                focus:ring-2
                focus:ring-indigo-500
              "
              placeholder="admin@example.com"
            />

          </div>

          {/* GENDER */}

          <div>

            <label
              className="
                text-sm
                font-medium
                text-gray-700
              "
            >
              Gender
            </label>

            <select
              value={gender}
              onChange={(e) =>
                setGender(
                  e.target.value
                )
              }
              className="
                mt-2
                w-full
                rounded-xl
                border
                px-4
                py-3
                outline-none
                focus:ring-2
                focus:ring-indigo-500
              "
            >

              <option>
                Male
              </option>

              <option>
                Female
              </option>

              <option>
                Other
              </option>

            </select>

          </div>

          {/* DOB */}

          <div>

            <label
              className="
                text-sm
                font-medium
                text-gray-700
              "
            >
              Date of Birth
            </label>

            <input
              type="date"
              value={dob}
              onChange={(e) =>
                setDob(
                  e.target.value
                )
              }
              className="
                mt-2
                w-full
                rounded-xl
                border
                px-4
                py-3
                outline-none
                focus:ring-2
                focus:ring-indigo-500
              "
            />

          </div>

          {/* ERROR */}

          {error && (

            <div
              className="
                rounded-xl
                bg-red-50
                border
                border-red-100
                px-4
                py-3
                text-sm
                text-red-700
              "
            >
              {error}
            </div>

          )}

          {/* SUCCESS */}

          {success && (

            <div
              className="
                rounded-xl
                bg-green-50
                border
                border-green-100
                px-4
                py-3
                text-sm
                text-green-700
              "
            >
              {success}
            </div>

          )}

        </div>

        {/* FOOTER */}

        <div
          className="
            flex
            justify-end
            gap-3
            border-t
            px-6
            py-5
          "
        >

          <button
            onClick={onClose}
            className="
              px-5
              py-3
              rounded-xl
              border
              font-medium
              hover:bg-gray-50
            "
          >
            Cancel
          </button>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="
              inline-flex
              items-center
              gap-2
              rounded-xl
              bg-indigo-600
              px-5
              py-3
              text-white
              font-medium
              hover:bg-indigo-700
              disabled:opacity-50
            "
          >

            {loading ? (

              <Loader2
                size={18}
                className="animate-spin"
              />

            ) : (

              <UserPlus size={18} />

            )}

            Create User

          </button>

        </div>

      </div>

    </div>
  )
}