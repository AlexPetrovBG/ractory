import { login } from '../services/auth';

export function renderLogin(container) {
  container.innerHTML = `
    <div class="flex items-center justify-center min-h-screen bg-slate-100">
      <div class="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
        <div>
          <h1 class="text-2xl font-bold text-center text-gray-900">Ra Factory</h1>
          <h2 class="mt-2 text-xl text-center text-gray-600">Admin Login</h2>
        </div>
        
        <div id="login-error" class="hidden p-4 text-sm text-white bg-red-500 rounded"></div>
        
        <form id="login-form" class="mt-8 space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
            <input id="email" name="email" type="email" required class="input mt-1" placeholder="admin@example.com">
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input id="password" name="password" type="password" required class="input mt-1" placeholder="••••••••">
          </div>
          
          <div>
            <button type="submit" class="w-full btn">
              <span id="login-button-text">Sign in</span>
              <span id="login-spinner" class="hidden ml-2">
                <svg class="w-4 h-4 text-white animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  `;

  // Attach event handlers
  const form = document.getElementById('login-form');
  const errorElement = document.getElementById('login-error');
  const buttonText = document.getElementById('login-button-text');
  const spinner = document.getElementById('login-spinner');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Show loading state
    buttonText.textContent = 'Signing in...';
    spinner.classList.remove('hidden');
    errorElement.classList.add('hidden');
    
    try {
      await login(email, password);
      // Redirect to dashboard on success
      window.location.href = '/';
    } catch (error) {
      // Show error message
      errorElement.textContent = error.message || 'Login failed. Please try again.';
      errorElement.classList.remove('hidden');
      
      // Reset button state
      buttonText.textContent = 'Sign in';
      spinner.classList.add('hidden');
    }
  });
} 