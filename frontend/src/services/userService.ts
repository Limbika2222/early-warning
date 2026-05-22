// src/services/userService.ts
import {
  sendPasswordResetEmail,
} from "firebase/auth"
import { auth } from "../firebase"

// =====================================================
// API BASE
// =====================================================

const API_BASE =
  import.meta.env.VITE_API_BASE

// =====================================================
// TYPES
// =====================================================

export interface CreateUserPayload {
  name: string
  email: string
  gender: string
  dob: string
}

// =====================================================

export interface UserResponse {
  success?: boolean
  message?: string
  uid?: string
  email?: string
  reset_link?: string
}

// =====================================================

export interface AdminUser {
  uid: string
  name: string
  email: string
  gender: string
  dob: string
  role: string
  is_active: boolean
  created_at?: string
}

// =====================================================
// CREATE SUB ADMIN
// =====================================================

export async function createSubAdmin(
  payload: CreateUserPayload
): Promise<UserResponse> {
  const response = await fetch(
    `${API_BASE}/api/admin/create-user`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to create user"
    )
  }

  return data
}

// =====================================================
// GET ALL USERS
// =====================================================

export async function getUsers(): Promise<AdminUser[]> {
  const response = await fetch(
    `${API_BASE}/api/admin/users`
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error("Failed to fetch users")
  }

  return data.users || []
}

// =====================================================
// DISABLE USER
// =====================================================

export async function disableUser(uid: string) {
  const response = await fetch(
    `${API_BASE}/api/admin/disable/${uid}`,
    {
      method: "PATCH",
    }
  )

  if (!response.ok) {
    throw new Error("Failed to disable user")
  }

  return response.json()
}

// =====================================================
// ENABLE USER
// =====================================================

export async function enableUser(uid: string) {
  const response = await fetch(
    `${API_BASE}/api/admin/enable/${uid}`,
    {
      method: "PATCH",
    }
  )

  if (!response.ok) {
    throw new Error("Failed to enable user")
  }

  return response.json()
}

// =====================================================
// DELETE USER
// =====================================================

export async function deleteUser(uid: string) {
  const response = await fetch(
    `${API_BASE}/api/admin/delete/${uid}`,
    {
      method: "DELETE",
    }
  )

  if (!response.ok) {
    throw new Error("Failed to delete user")
  }

  return response.json()
}

// =====================================================
// SEND PASSWORD RESET EMAIL
// =====================================================

export async function sendResetEmail(
  email: string
) {

  try {

    await sendPasswordResetEmail(

      auth,

      email
    )

    return {

      success: true,

      message:
        "Password reset email sent",
    }

  } catch (error) {

    console.error(
      "RESET EMAIL ERROR:",
      error
    )

    throw error
  }
}
