// Determine API URL based on current environment
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api/v1'
  : `https://rafactory.raworkshop.bg/api/v1`;

// Get the stored auth data
export function getAuthData() {
  const authData = localStorage.getItem('auth');
  return authData ? JSON.parse(authData) : null;
}

// Check if the user is authenticated
export async function checkAuth() {
  const authData = getAuthData();
  if (!authData || !authData.access_token) return false;
  
  // Check if token is expired
  const expiry = new Date(authData.expires_at);
  const now = new Date();
  
  if (now >= expiry) {
    try {
      // Try to refresh the token
      const refreshed = await refreshToken(authData.refresh_token);
      return !!refreshed;
    } catch (error) {
      console.error('Error refreshing token:', error);
      logout();
      return false;
    }
  }
  
  return true;
}

// Login the user
export async function login(email, password) {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }
    
    const data = await response.json();
    
    // Calculate token expiry (15 minutes from now)
    const expiresAt = new Date();
    expiresAt.setSeconds(expiresAt.getSeconds() + data.expires_in);
    
    // Store auth data
    const authData = {
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      role: data.role,
      expires_at: expiresAt.toISOString()
    };
    
    localStorage.setItem('auth', JSON.stringify(authData));
    return authData;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

// Refresh the access token
export async function refreshToken(refreshToken) {
  try {
    const response = await fetch(`${API_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    
    if (!response.ok) {
      throw new Error('Refresh token failed');
    }
    
    const data = await response.json();
    
    // Calculate token expiry
    const expiresAt = new Date();
    expiresAt.setSeconds(expiresAt.getSeconds() + data.expires_in);
    
    // Update auth data
    const authData = getAuthData();
    authData.access_token = data.access_token;
    authData.expires_at = expiresAt.toISOString();
    
    localStorage.setItem('auth', JSON.stringify(authData));
    return authData;
  } catch (error) {
    console.error('Token refresh error:', error);
    logout();
    throw error;
  }
}

// Logout the user
export function logout() {
  localStorage.removeItem('auth');
  window.location.href = '/login';
}

// Get the authorization header
export function getAuthHeader() {
  const authData = getAuthData();
  return authData?.access_token 
    ? { 'Authorization': `Bearer ${authData.access_token}` } 
    : {};
} 