import './style.css';
import { createRouter } from './utils/router';
import { checkAuth } from './services/auth';

// Initialize the app
document.addEventListener('DOMContentLoaded', async () => {
  // Check if the user is authenticated
  const isAuthenticated = await checkAuth();
  
  if (!isAuthenticated && window.location.pathname !== '/login') {
    window.location.href = '/login';
    return;
  }

  // Set up the router
  createRouter();
}); 