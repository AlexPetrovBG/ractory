import { renderNavbar } from '../components/navbar';
import { getAuthData } from '../services/auth';
import { dashboardApi, userApi } from '../services/api';

export async function renderDashboard(container) {
  const authData = getAuthData();
  
  // Initial render with loading state
  container.innerHTML = `
    <div class="min-h-screen bg-slate-100">
      ${renderNavbar()}
      
      <main class="container px-4 py-8 mx-auto max-w-7xl">
        <header class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        </header>
        
        <div class="mb-6 p-6 bg-white rounded-lg shadow-md">
          <div id="company-info-container">
            <div class="flex items-center">
              <div class="w-14 h-14 bg-primary-100 rounded-full flex items-center justify-center mr-4">
                <span class="text-xl font-bold text-primary-700">...</span>
              </div>
              <div>
                <h2 class="text-2xl font-semibold text-gray-800">Loading...</h2>
                <p class="text-gray-500">Loading company information...</p>
              </div>
              <div class="ml-auto">
                <span class="px-3 py-1 text-sm rounded-full bg-gray-200 text-gray-600">Loading...</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div class="p-6 bg-white rounded-lg shadow-md">
            <h2 class="text-xl font-semibold text-gray-800">Users</h2>
            <p id="users-count" class="mt-2 text-4xl font-bold text-primary-600">
              <span class="inline-block w-6 h-6 animate-pulse bg-primary-200 rounded"></span>
            </p>
            <a href="/users" class="inline-block mt-4 text-sm text-primary-600 hover:text-primary-800">Manage Users →</a>
          </div>
          
          <div class="p-6 bg-white rounded-lg shadow-md">
            <h2 class="text-xl font-semibold text-gray-800">Companies</h2>
            <p id="companies-count" class="mt-2 text-4xl font-bold text-primary-600">
              <span class="inline-block w-6 h-6 animate-pulse bg-primary-200 rounded"></span>
            </p>
            <a href="/companies" class="inline-block mt-4 text-sm text-primary-600 hover:text-primary-800">Manage Companies →</a>
          </div>
          
          <div class="p-6 bg-white rounded-lg shadow-md">
            <h2 class="text-xl font-semibold text-gray-800">Projects</h2>
            <p id="projects-count" class="mt-2 text-4xl font-bold text-primary-600">
              <span class="inline-block w-6 h-6 animate-pulse bg-primary-200 rounded"></span>
            </p>
            <a href="/projects" class="inline-block mt-4 text-sm text-primary-600 hover:text-primary-800">View Projects →</a>
          </div>
          
          <div class="p-6 bg-white rounded-lg shadow-md">
            <h2 class="text-xl font-semibold text-gray-800">Workstations</h2>
            <p id="workstations-count" class="mt-2 text-4xl font-bold text-primary-600">
              <span class="inline-block w-6 h-6 animate-pulse bg-primary-200 rounded"></span>
            </p>
            <a href="/workstations" class="inline-block mt-4 text-sm text-primary-600 hover:text-primary-800">Manage Workstations →</a>
          </div>
        </div>
        
        <div class="p-6 mt-6 bg-white rounded-lg shadow-md">
          <h2 class="text-xl font-semibold text-gray-800">Recent Activity</h2>
          <div id="activity-container" class="mt-4 text-gray-600">
            <div class="flex items-center justify-center py-4">
              <svg class="w-5 h-5 text-primary-500 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <div class="p-6 mt-6 bg-white rounded-lg shadow-md">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-800">User List</h2>
            <a href="/users" class="text-sm text-primary-600 hover:text-primary-800">View All →</a>
          </div>
          <div id="users-list-container" class="mt-4">
            <div class="flex items-center justify-center py-4">
              <svg class="w-5 h-5 text-primary-500 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;

  try {
    // Fetch company info
    try {
      const companyInfo = await dashboardApi.getCompanyInfo();
      const companyContainer = document.getElementById('company-info-container');
      
      if (companyInfo) {
        companyContainer.innerHTML = `
          <div class="flex items-center">
            <div class="w-14 h-14 bg-primary-100 rounded-full flex items-center justify-center mr-4">
              <span class="text-xl font-bold text-primary-700">${companyInfo.short_name?.substring(0, 2) || companyInfo.name?.substring(0, 2) || '??'}</span>
            </div>
            <div>
              <h2 class="text-2xl font-semibold text-gray-800">${companyInfo.name || 'Unknown Company'}</h2>
              <p class="text-gray-500">
                ${companyInfo.subscription_tier || 'No'} Plan
                ${companyInfo.created_at ? `· Since ${new Date(companyInfo.created_at).toLocaleDateString()}` : ''}
              </p>
            </div>
            <div class="ml-auto">
              <span class="px-3 py-1 text-sm rounded-full 
                ${companyInfo.subscription_status === 'active' ? 'bg-green-100 text-green-800' : 
                  companyInfo.subscription_status === 'trial' ? 'bg-yellow-100 text-yellow-800' : 
                  'bg-red-100 text-red-800'}">
                ${companyInfo.subscription_status === 'active' ? 'Active' : 
                  companyInfo.subscription_status === 'trial' ? 'Trial' : 
                  'Inactive'}
              </span>
            </div>
          </div>
        `;
      } else {
        companyContainer.innerHTML = `
          <div class="p-4 border border-gray-200 rounded-md">
            <p class="text-center text-gray-500">Company information not available</p>
          </div>
        `;
      }
    } catch (error) {
      console.error('Error fetching company info:', error);
      document.getElementById('company-info-container').innerHTML = `
        <div class="p-4 border border-red-200 rounded-md">
          <p class="text-center text-red-500">Error loading company information</p>
        </div>
      `;
    }
    
    // Fetch dashboard counts
    const counts = await dashboardApi.getDashboardCounts();
    
    // Update the counts in the UI
    document.getElementById('users-count').textContent = counts.users;
    document.getElementById('companies-count').textContent = counts.companies;
    document.getElementById('projects-count').textContent = counts.projects;
    document.getElementById('workstations-count').textContent = counts.workstations;
    
    // Try to fetch recent activity
    try {
      const activity = await dashboardApi.getRecentActivity();
      
      const activityContainer = document.getElementById('activity-container');
      
      if (activity && activity.length > 0) {
        // Render activity items
        activityContainer.innerHTML = `
          <ul class="divide-y divide-gray-200">
            ${activity.map(item => `
              <li class="py-3">
                <div class="flex items-start">
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center justify-center h-8 w-8 rounded-full bg-primary-100">
                      <span class="text-sm font-medium text-primary-800">${item.user?.substring(0, 1) || '?'}</span>
                    </span>
                  </div>
                  <div class="ml-4">
                    <p class="text-sm font-medium text-gray-900">${item.action || 'Action'}</p>
                    <p class="text-sm text-gray-500">${item.details || ''}</p>
                    <p class="mt-1 text-xs text-gray-400">${new Date(item.timestamp).toLocaleString()}</p>
                  </div>
                </div>
              </li>
            `).join('')}
          </ul>
        `;
      } else {
        // No activity
        activityContainer.innerHTML = `
          <p>No recent activity to display.</p>
        `;
      }
    } catch (error) {
      console.error('Error rendering activity:', error);
      document.getElementById('activity-container').innerHTML = `
        <p>No recent activity to display.</p>
      `;
    }
    
    // Fetch and display users
    try {
      const users = await userApi.getUsers(1, 5); // Get first 5 users
      const usersContainer = document.getElementById('users-list-container');
      
      if (users && users.length > 0) {
        // Render user list
        usersContainer.innerHTML = `
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                ${users.map(user => `
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                          <span class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-primary-100">
                            <span class="font-medium text-primary-800">${user.email?.substring(0, 1).toUpperCase() || '?'}</span>
                          </span>
                        </div>
                        <div class="ml-4">
                          <div class="text-sm font-medium text-gray-900">${user.email || 'Unknown Email'}</div>
                          <div class="text-sm text-gray-500">${user.guid || ''}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-900">${user.role || 'N/A'}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                        ${user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;
      } else {
        // No users
        usersContainer.innerHTML = `
          <p class="text-center py-4">No users found.</p>
        `;
      }
    } catch (error) {
      console.error('Error fetching users:', error);
      document.getElementById('users-list-container').innerHTML = `
        <p class="text-center py-4 text-red-600">Error loading users. Please try again.</p>
      `;
    }
    
  } catch (error) {
    console.error('Error rendering dashboard:', error);
    
    // Set error or fallback values
    document.getElementById('company-info-container').innerHTML = `
      <div class="p-4 border border-red-200 rounded-md">
        <p class="text-center text-red-500">Error loading company information</p>
      </div>
    `;
    document.getElementById('users-count').textContent = '?';
    document.getElementById('companies-count').textContent = '?';
    document.getElementById('projects-count').textContent = '?';
    document.getElementById('workstations-count').textContent = '?';
    document.getElementById('activity-container').innerHTML = `
      <p>No recent activity to display.</p>
    `;
    document.getElementById('users-list-container').innerHTML = `
      <p class="text-center py-4">Unable to load users.</p>
    `;
  }
} 