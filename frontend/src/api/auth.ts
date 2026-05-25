const API_BASE =
  "https://8000-firebase-early-warning-1772198111524.cluster-fdkw7vjj7bgguspe3fbbc25tra.cloudworkstations.dev"

export interface LoginResponse {

  access_token: string

  token_type: string

  user: {

    id: number

    name: string

    email: string

    role: string
  }
}

export async function loginUser(

  email: string,

  password: string
): Promise<LoginResponse> {

  const response = await fetch(

    `${API_BASE}/api/auth/login`,

    {

      method: "POST",

      headers: {

        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({

        email,

        password,
      }),
    }
  )

  if (!response.ok) {

    const error =
      await response.json()

    throw new Error(

      error.detail ||

      "Login failed"
    )
  }

  return response.json()
}