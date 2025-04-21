import { renderLogin } from '../pages/login';
import { renderDashboard } from '../pages/dashboard';
import { renderUsers } from '../pages/users';
import { renderCompanies } from '../pages/companies';

const routes = {
  '/': renderDashboard,
  '/login': renderLogin,
  '/users': renderUsers,
  '/companies': renderCompanies,
};

export function createRouter() {
  const appElement = document.getElementById('app');
  
  // Function to render a page, handling async functions
  async function renderRoute(path) {
    const renderPage = routes[path] || routes['/'];
    
    // Check if the render function is async
    if (renderPage.constructor.name === 'AsyncFunction') {
      try {
        await renderPage(appElement);
      } catch (error) {
        console.error('Error rendering page:', error);
        appElement.innerHTML = `
          <div class="flex items-center justify-center min-h-screen">
            <div class="p-6 bg-white rounded-lg shadow-md">
              <h2 class="text-xl font-semibold text-red-600">Error Loading Page</h2>
              <p class="mt-2 text-gray-600">There was an error loading this page. Please try again.</p>
              <button onclick="window.location.reload()" class="px-4 py-2 mt-4 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700">
                Reload
              </button>
            </div>
          </div>
        `;
      }
    } else {
      // Handle synchronous render functions
      renderPage(appElement);
    }
  }
  
  // Initial render
  const pathname = window.location.pathname || '/';
  renderRoute(pathname);
  
  // Handle navigation
  document.addEventListener('click', (event) => {
    const target = event.target.closest('a');
    if (target && target.getAttribute('href')?.startsWith('/')) {
      event.preventDefault();
      const path = target.getAttribute('href');
      
      // Update URL without reload
      window.history.pushState({}, '', path);
      
      // Render the new page
      renderRoute(path);
    }
  });
  
  // Handle back/forward navigation
  window.addEventListener('popstate', () => {
    const path = window.location.pathname;
    renderRoute(path);
  });
} 