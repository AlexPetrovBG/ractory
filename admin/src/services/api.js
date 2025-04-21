import { getAuthHeader, refreshToken, logout } from './auth';

// Determine API URL based on current environment
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api/v1'
  : `https://rafactory.raworkshop.bg/api/v1`;

// Helper function to handle API responses
async function handleResponse(response) {
  if (response.ok) {
    if (response.status === 204) {
      return null;
    }
    return await response.json();
  }

  // Handle 401 Unauthorized - try to refresh token once
  if (response.status === 401) {
    try {
      const authData = localStorage.getItem('auth');
      if (authData) {
        const { refresh_token } = JSON.parse(authData);
        await refreshToken(refresh_token);
        
        // Retry the request with the new token
        const originalRequest = response.url;
        const method = response.method;
        const headers = {
          'Content-Type': 'application/json',
          ...getAuthHeader()
        };
        
        // TODO: This is a simplified retry and doesn't preserve the original body
        const retryResponse = await fetch(originalRequest, { method, headers });
        return handleResponse(retryResponse);
      }
    } catch (error) {
      console.error('Failed to refresh token:', error);
      logout();
      throw new Error('Session expired. Please login again.');
    }
  }

  // Handle other errors
  const error = await response.json().catch(() => ({ detail: 'An unknown error occurred' }));
  throw new Error(error.detail || response.statusText);
}

// Generic fetch function with authentication
async function fetchWithAuth(endpoint, options = {}) {
  const url = `${API_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...getAuthHeader(),
    ...options.headers
  };

  const response = await fetch(url, {
    ...options,
    headers
  });

  return handleResponse(response);
}

// Dashboard API functions
export const dashboardApi = {
  // Get dashboard counts
  async getDashboardCounts() {
    try {
      // In a real app, we might have a dedicated endpoint for dashboard counts
      // For now, we'll make multiple requests and combine the data
      const [usersResponse, projectsResponse, workstationsResponse, companiesResponse] = await Promise.allSettled([
        fetchWithAuth('/users?page=1&size=1'),
        fetchWithAuth('/projects?page=1&size=1'),
        fetchWithAuth('/workstations?page=1&size=1'),
        fetchWithAuth('/companies')
      ]);
      
      // Extract counts from headers or response data
      // This is simplified and would depend on the actual API response structure
      return {
        users: usersResponse.status === 'fulfilled' ? 
          (usersResponse.value?.total_count || usersResponse.value?.length || '?') : '?',
        projects: projectsResponse.status === 'fulfilled' ? 
          (projectsResponse.value?.total_count || projectsResponse.value?.length || '?') : '?',
        workstations: workstationsResponse.status === 'fulfilled' ? 
          (workstationsResponse.value?.total_count || workstationsResponse.value?.length || '?') : '?',
        companies: companiesResponse.status === 'fulfilled' ? 
          (companiesResponse.value?.total_count || companiesResponse.value?.length || '?') : '?'
      };
    } catch (error) {
      console.error('Error fetching dashboard counts:', error);
      return { users: '?', projects: '?', workstations: '?', companies: '?' };
    }
  },
  
  // Get company info
  async getCompanyInfo() {
    try {
      return await fetchWithAuth('/companies/current');
    } catch (error) {
      console.error('Error fetching company info:', error);
      return null;
    }
  },
  
  // Get recent activity
  async getRecentActivity(limit = 5) {
    try {
      // In a real app, we'd have an endpoint for recent activity
      // This is a placeholder
      return fetchWithAuth(`/activity?limit=${limit}`);
    } catch (error) {
      console.error('Error fetching recent activity:', error);
      return [];
    }
  }
};

// User API functions
export const userApi = {
  // Get list of users
  async getUsers(page = 1, size = 10) {
    return fetchWithAuth(`/users?page=${page}&size=${size}`);
  },

  // Get a single user
  async getUser(id) {
    return fetchWithAuth(`/users/${id}`);
  },

  // Create a new user
  async createUser(userData) {
    return fetchWithAuth('/users', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  },

  // Update a user
  async updateUser(id, userData) {
    return fetchWithAuth(`/users/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(userData)
    });
  },

  // Delete a user
  async deleteUser(id) {
    return fetchWithAuth(`/users/${id}`, {
      method: 'DELETE'
    });
  }
};

// Company API functions
export const companiesApi = {
  // Get list of companies
  async getCompanies(page = 1, size = 10) {
    try {
      return await fetchWithAuth(`/companies?page=${page}&size=${size}`);
    } catch (error) {
      console.error('Error fetching companies:', error);
      if (error.message.includes('Not Found')) {
        // For now, return the current company in an array since we only have /companies/current
        const currentCompany = await this.getCurrentCompany();
        return currentCompany ? [currentCompany] : [];
      }
      throw error;
    }
  },

  // Get current company
  async getCurrentCompany() {
    return fetchWithAuth('/companies/current');
  },

  // Get a single company
  async getCompany(id) {
    return fetchWithAuth(`/companies/${id}`);
  },

  // Create a new company
  async createCompany(companyData) {
    return fetchWithAuth('/companies', {
      method: 'POST',
      body: JSON.stringify(companyData)
    });
  },

  // Update a company
  async updateCompany(id, companyData) {
    return fetchWithAuth(`/companies/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(companyData)
    });
  },

  // Delete a company
  async deleteCompany(id) {
    return fetchWithAuth(`/companies/${id}`, {
      method: 'DELETE'
    });
  }
}; 