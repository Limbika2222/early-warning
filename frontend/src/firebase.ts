// frontend/src/firebase.ts

import { initializeApp } from "firebase/app"
import {
  getAuth,
  setPersistence,
  browserLocalPersistence,
} from "firebase/auth"

const firebaseConfig = {
  apiKey: "AIzaSyDweWBXLwU5EKItfI5_EQRvKw5EAjgzB9o",
  authDomain: "early-warning-dashboard.firebaseapp.com",
  projectId: "early-warning-dashboard",
  storageBucket: "early-warning-dashboard.firebasestorage.app",
  messagingSenderId: "134687114838",
  appId: "1:134687114838:web:fc401dc77eea6fce52ddf7",
}

const app = initializeApp(firebaseConfig)

export const auth = getAuth(app)

// ✅ Keep user logged in across refresh
setPersistence(auth, browserLocalPersistence).catch((err) => {
  console.error("Persistence error:", err)
})