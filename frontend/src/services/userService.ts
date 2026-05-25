const API_BASE =
  "https://8000-firebase-early-warning-1772198111524.cluster-fdkw7vjj7bgguspe3fbbc25tra.cloudworkstations.dev"

// =====================================================
// TYPES
// =====================================================

export interface User {

  id: number

  name: string

  email: string

  role: string

  is_active: boolean
}

// =====================================================
// GET USERS
// =====================================================

export async function getUsers():

Promise<User[]> {

  const response = await fetch(

    `${API_BASE}/api/admin/users`
  )

  if (!response.ok) {

    throw new Error(
      "Failed to fetch users"
    )
  }

  const data =
    await response.json()

  return data.users
}

// =====================================================
// CREATE SUB ADMIN
// =====================================================

export async function createSubAdmin(

  payload: {

    name: string

    email: string

    gender: string

    dob: string
  }
) {

  const response = await fetch(

    `${API_BASE}/api/admin/create-user`,

    {

      method: "POST",

      headers: {

        "Content-Type":
          "application/json",
      },

      body: JSON.stringify(
        payload
      ),
    }
  )

  if (!response.ok) {

    const error =
      await response.json()

    throw new Error(

      error.detail ||

      "Failed to create user"
    )
  }

  return response.json()
}

// =====================================================
// DELETE USER
// =====================================================

export async function deleteUser(
  userId: number
) {

  const response = await fetch(

    `${API_BASE}/api/admin/delete/${userId}`,

    {
      method: "DELETE",
    }
  )

  if (!response.ok) {

    throw new Error(
      "Failed to delete user"
    )
  }

  return response.json()
}

// =====================================================
// DISABLE USER
// =====================================================

export async function disableUser(
  userId: number
) {

  const response = await fetch(

    `${API_BASE}/api/admin/disable/${userId}`,

    {
      method: "PATCH",
    }
  )

  if (!response.ok) {

    throw new Error(
      "Failed to disable user"
    )
  }

  return response.json()
}

// =====================================================
// ENABLE USER
// =====================================================

export async function enableUser(
  userId: number
) {

  const response = await fetch(

    `${API_BASE}/api/admin/enable/${userId}`,

    {
      method: "PATCH",
    }
  )

  if (!response.ok) {

    throw new Error(
      "Failed to enable user"
    )
  }

  return response.json()
}

// =====================================================
// SEND RESET EMAIL
// =====================================================

export async function sendResetEmail(
  email: string
) {

  const response = await fetch(

    `${API_BASE}/api/admin/reset-password`,

    {

      method: "POST",

      headers: {

        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({

        email,
      }),
    }
  )

  if (!response.ok) {

    throw new Error(
      "Failed to send reset email"
    )
  }

  return response.json()
}
