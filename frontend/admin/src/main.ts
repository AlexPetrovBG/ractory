import './style.css'
import { initializeLayout, loadContent } from './layout'
import { showLoginPage, handleLogin } from './auth'
import { createApiClient } from './api'

const appElement = document.getElementById('app')
const apiClient = createApiClient() // Create API client instance

if (!appElement) {
    throw new Error("Root element #app not found")
}

const checkAuth = async () => {
    const token = localStorage.getItem('access_token') // Or get from secure cookie/state

    if (!token) {
        showLoginPage(appElement, handleLogin) // Show login if no token
        return false
    }

    // Optional: Verify token validity with a backend endpoint (e.g., /users/me)
    try {
        // Uncomment and adjust when backend is ready
        // await apiClient.get('/users/me') // Throws if token is invalid/expired
        return true
    } catch (error) {
        console.error("Token validation failed:", error)
        localStorage.removeItem('access_token')
        showLoginPage(appElement, handleLogin)
        return false
    }
}

const initApp = async () => {
    const isAuthenticated = await checkAuth()

    if (isAuthenticated) {
        initializeLayout(appElement)
        // Load initial page (e.g., dashboard or user list)
        loadContent('<h1>Dashboard Coming Soon...</h1>')
        // Setup navigation listeners here (covered later)
    }
}

initApp()
