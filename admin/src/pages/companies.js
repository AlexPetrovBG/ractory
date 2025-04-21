import { renderNavbar } from '../components/navbar';
import { getAuthData } from '../services/auth';
import { companiesApi } from '../services/api';

export async function renderCompanies(container) {
  const authData = getAuthData();
  
  // Initial render with loading state
  container.innerHTML = `
    <div class="min-h-screen bg-slate-100">
      ${renderNavbar()}
      
      <main class="container px-4 py-8 mx-auto max-w-7xl">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Companies</h1>
          <button id="add-company-btn" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            <svg class="mr-2 -ml-1 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Add Company
          </button>
        </div>
        
        <div class="bg-white shadow overflow-hidden sm:rounded-md">
          <div id="companies-list" class="divide-y divide-gray-200">
            <div class="p-4 text-center text-gray-500">
              <svg class="mx-auto h-8 w-8 text-gray-400 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p class="mt-2">Loading companies...</p>
            </div>
          </div>
        </div>
        
        <!-- Company Modal -->
        <div id="company-modal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center hidden">
          <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div class="flex justify-between items-center mb-4">
              <h2 id="modal-title" class="text-xl font-semibold text-gray-900">Add Company</h2>
              <button id="close-modal-btn" class="text-gray-400 hover:text-gray-500">
                <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <form id="company-form" class="space-y-4">
              <input type="hidden" id="company-id">
              <div>
                <label for="company-name" class="block text-sm font-medium text-gray-700">Company Name</label>
                <input type="text" id="company-name" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
              </div>
              <div>
                <label for="company-short-name" class="block text-sm font-medium text-gray-700">Short Name</label>
                <input type="text" id="company-short-name" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
              </div>
              <div>
                <label for="subscription-tier" class="block text-sm font-medium text-gray-700">Subscription Tier</label>
                <select id="subscription-tier" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                  <option value="Basic">Basic</option>
                  <option value="Professional">Professional</option>
                  <option value="Enterprise">Enterprise</option>
                </select>
              </div>
              <div>
                <label for="subscription-status" class="block text-sm font-medium text-gray-700">Status</label>
                <select id="subscription-status" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                  <option value="active">Active</option>
                  <option value="trial">Trial</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
              <div class="flex justify-end space-x-3 pt-4">
                <button type="button" id="cancel-btn" class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  Cancel
                </button>
                <button type="submit" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
        
        <!-- Delete Confirmation Modal -->
        <div id="delete-confirm-modal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center hidden">
          <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div class="mb-4">
              <h2 class="text-xl font-semibold text-gray-900">Confirm Deletion</h2>
              <p class="mt-2 text-gray-600">Are you sure you want to delete this company? This action cannot be undone.</p>
            </div>
            <div class="flex justify-end space-x-3">
              <button id="cancel-delete-btn" class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                Cancel
              </button>
              <button id="confirm-delete-btn" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                Delete
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  `;

  try {
    // Fetch companies
    const companies = await companiesApi.getCompanies();
    
    const companiesList = document.getElementById('companies-list');
    
    if (companies && companies.length > 0) {
      companiesList.innerHTML = `
        <ul class="divide-y divide-gray-200">
          ${companies.map(company => `
            <li class="p-4 hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-12 w-12 bg-primary-100 rounded-full flex items-center justify-center">
                    <span class="text-lg font-semibold text-primary-800">${company.short_name?.substring(0, 2) || company.name?.substring(0, 2) || '??'}</span>
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-medium text-gray-900">${company.name}</h3>
                    <div class="flex items-center text-sm text-gray-500">
                      <span class="mr-2">${company.subscription_tier || 'No'} Plan</span>
                      <span class="px-2 py-0.5 text-xs rounded-full 
                        ${company.subscription_status === 'active' ? 'bg-green-100 text-green-800' : 
                          company.subscription_status === 'trial' ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-red-100 text-red-800'}">
                        ${company.subscription_status === 'active' ? 'Active' : 
                          company.subscription_status === 'trial' ? 'Trial' : 
                          'Inactive'}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="flex space-x-2">
                  <button class="edit-company-btn p-1 text-gray-400 hover:text-primary-600" data-id="${company.guid}">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button class="delete-company-btn p-1 text-gray-400 hover:text-red-600" data-id="${company.guid}">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </li>
          `).join('')}
        </ul>
      `;
    } else {
      companiesList.innerHTML = `
        <div class="p-6 text-center">
          <p class="text-gray-500">No companies found</p>
          <button id="no-companies-add-btn" class="mt-2 inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-600 border border-primary-300 rounded-md hover:bg-primary-50">
            <svg class="mr-1 -ml-0.5 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Add Your First Company
          </button>
        </div>
      `;
      
      document.getElementById('no-companies-add-btn')?.addEventListener('click', () => openModal());
    }
    
    // Add event listeners
    setupEventListeners(companies);
    
  } catch (error) {
    console.error('Error rendering companies page:', error);
    
    document.getElementById('companies-list').innerHTML = `
      <div class="p-6 text-center">
        <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <p class="mt-2 text-gray-500">Error loading companies</p>
      </div>
    `;
  }

  function setupEventListeners(companies) {
    // Add company button
    document.getElementById('add-company-btn')?.addEventListener('click', () => openModal());
    
    // Edit buttons
    document.querySelectorAll('.edit-company-btn').forEach(button => {
      button.addEventListener('click', async () => {
        const companyId = button.getAttribute('data-id');
        const company = companies.find(c => c.guid === companyId);
        if (company) {
          openModal(company);
        }
      });
    });
    
    // Delete buttons
    document.querySelectorAll('.delete-company-btn').forEach(button => {
      button.addEventListener('click', () => {
        const companyId = button.getAttribute('data-id');
        openDeleteModal(companyId);
      });
    });
    
    // Close modal buttons
    document.getElementById('close-modal-btn')?.addEventListener('click', closeModal);
    document.getElementById('cancel-btn')?.addEventListener('click', closeModal);
    
    // Cancel delete button
    document.getElementById('cancel-delete-btn')?.addEventListener('click', closeDeleteModal);
    
    // Form submission
    document.getElementById('company-form')?.addEventListener('submit', handleFormSubmit);
    
    // Delete confirmation
    document.getElementById('confirm-delete-btn')?.addEventListener('click', handleDeleteConfirm);
  }
  
  function openModal(company = null) {
    const modal = document.getElementById('company-modal');
    const modalTitle = document.getElementById('modal-title');
    const form = document.getElementById('company-form');
    const idInput = document.getElementById('company-id');
    const nameInput = document.getElementById('company-name');
    const shortNameInput = document.getElementById('company-short-name');
    const tierSelect = document.getElementById('subscription-tier');
    const statusSelect = document.getElementById('subscription-status');
    
    // Clear form first
    form.reset();
    
    if (company) {
      // Edit mode
      modalTitle.textContent = 'Edit Company';
      idInput.value = company.guid;
      nameInput.value = company.name || '';
      shortNameInput.value = company.short_name || '';
      tierSelect.value = company.subscription_tier || 'Basic';
      statusSelect.value = company.subscription_status || 'active';
    } else {
      // Add mode
      modalTitle.textContent = 'Add Company';
      idInput.value = '';
    }
    
    modal.classList.remove('hidden');
  }
  
  function closeModal() {
    document.getElementById('company-modal').classList.add('hidden');
  }
  
  function openDeleteModal(companyId) {
    document.getElementById('delete-confirm-modal').classList.remove('hidden');
    document.getElementById('confirm-delete-btn').setAttribute('data-id', companyId);
  }
  
  function closeDeleteModal() {
    document.getElementById('delete-confirm-modal').classList.add('hidden');
  }
  
  async function handleFormSubmit(event) {
    event.preventDefault();
    
    const idInput = document.getElementById('company-id');
    const nameInput = document.getElementById('company-name');
    const shortNameInput = document.getElementById('company-short-name');
    const tierSelect = document.getElementById('subscription-tier');
    const statusSelect = document.getElementById('subscription-status');
    
    const companyData = {
      name: nameInput.value.trim(),
      short_name: shortNameInput.value.trim(),
      subscription_tier: tierSelect.value,
      subscription_status: statusSelect.value
    };
    
    try {
      if (idInput.value) {
        // Update existing company
        await companiesApi.updateCompany(idInput.value, companyData);
      } else {
        // Create new company
        await companiesApi.createCompany(companyData);
      }
      
      // Refresh the page to show updated data
      window.location.reload();
    } catch (error) {
      console.error('Error saving company:', error);
      alert('Failed to save company. Please try again.');
    }
  }
  
  async function handleDeleteConfirm() {
    const deleteBtn = document.getElementById('confirm-delete-btn');
    const companyId = deleteBtn.getAttribute('data-id');
    
    if (!companyId) return;
    
    try {
      await companiesApi.deleteCompany(companyId);
      
      // Refresh the page to show updated data
      window.location.reload();
    } catch (error) {
      console.error('Error deleting company:', error);
      alert('Failed to delete company. Please try again.');
      closeDeleteModal();
    }
  }
} 