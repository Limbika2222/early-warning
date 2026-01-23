// frontend/src/firebase.ts

import { initializeApp } from "firebase/app"
import { getAuth } from "firebase/auth"

// Firebase configuration (use .env in future, but this works for now)
const firebaseConfig = {
  apiKey: "AIzaSyDweWBXLwU5EKItfI5_EQRvKw5EAjgzB9o",
  authDomain: "early-warning-dashboard.firebaseapp.com",
  projectId: "early-warning-dashboard",
  storageBucket: "early-warning-dashboard.firebasestorage.app",
  messagingSenderId: "134687114838",
  appId: "1:134687114838:web:fc401dc77eea6fce52ddf7",
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)

// ✅ Initialize and export Auth
export const auth = getAuth(app)
