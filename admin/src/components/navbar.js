import { logout, getAuthData } from '../services/auth';

export function renderNavbar() {
  const authData = getAuthData();
  const role = authData?.role || 'Guest';
  
  return `
    <nav class="bg-white shadow">
      <div class="container px-4 mx-auto max-w-7xl">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <a href="/" class="flex items-center flex-shrink-0">
              <span class="text-xl font-bold text-primary-600">Ra Factory</span>
            </a>
            <div class="hidden md:block">
              <div class="flex items-baseline ml-10 space-x-4">
                <a href="/" class="px-3 py-2 text-sm font-medium text-gray-900 rounded-md hover:bg-slate-100">Dashboard</a>
                <a href="/users" class="px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-slate-100 hover:text-gray-900">Users</a>
                <a href="/projects" class="px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-slate-100 hover:text-gray-900">Projects</a>
                <a href="/workstations" class="px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-slate-100 hover:text-gray-900">Workstations</a>
              </div>
            </div>
          </div>
          <div class="flex items-center">
            <div class="hidden md:block">
              <span class="mr-4 text-sm text-gray-600">${role}</span>
            </div>
            <button id="logout-button" class="px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-slate-100 hover:text-gray-900">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  `;
  
  // Add event listener after rendering
  setTimeout(() => {
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
      logoutButton.addEventListener('click', () => {
        logout();
      });
    }
  }, 0);
} 