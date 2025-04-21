import { renderNavbar } from '../components/navbar';
import { userApi } from '../services/api';

const userRoles = ['CompanyAdmin', 'ProjectManager', 'Operator'];

export async function renderUsers(container) {
  // Show loading state
  container.innerHTML = `
    <div class="min-h-screen bg-slate-100">
      ${renderNavbar()}
      
      <main class="container px-4 py-8 mx-auto max-w-7xl">
        <div class="flex items-center justify-between mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Users</h1>
          <button id="new-user-button" class="btn">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path>
            </svg>
            New User
          </button>
        </div>
        
        <div id="users-list" class="p-6 bg-white rounded-lg shadow-md">
          <div class="flex items-center justify-center p-8">
            <svg class="w-8 h-8 text-primary-500 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        </div>
      </main>
      
      <!-- User Modal (hidden by default) -->
      <div id="user-modal" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="absolute inset-0 bg-black opacity-50" id="modal-backdrop"></div>
        <div class="z-10 w-full max-w-md p-8 mx-4 bg-white rounded-lg shadow-xl">
          <h2 id="modal-title" class="text-2xl font-bold text-gray-900">Add New User</h2>
          
          <form id="user-form" class="mt-6 space-y-4">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input id="user-email" type="email" required class="input mt-1" placeholder="user@example.com">
            </div>
            
            <div>
              <label for="role" class="block text-sm font-medium text-gray-700">Role</label>
              <select id="user-role" class="input mt-1">
                ${userRoles.map(role => `<option value="${role}">${role}</option>`).join('')}
              </select>
            </div>
            
            <div id="pin-container">
              <label for="pin" class="block text-sm font-medium text-gray-700">PIN (only for Operators)</label>
              <input id="user-pin" type="text" pattern="[0-9]{6}" class="input mt-1" placeholder="123456" maxlength="6">
              <p class="mt-1 text-xs text-gray-500">6-digit PIN code for operator logins</p>
            </div>
            
            <div class="pt-4 mt-6 border-t border-gray-200">
              <div class="flex justify-end space-x-3">
                <button type="button" id="cancel-button" class="btn-secondary">Cancel</button>
                <button type="submit" id="save-button" class="btn">
                  <span id="save-button-text">Save</span>
                  <span id="save-spinner" class="hidden ml-2">
                    <svg class="w-4 h-4 text-white animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
      
      <!-- Confirm Delete Modal -->
      <div id="delete-modal" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="absolute inset-0 bg-black opacity-50"></div>
        <div class="z-10 w-full max-w-md p-8 mx-4 bg-white rounded-lg shadow-xl">
          <h2 class="text-2xl font-bold text-gray-900">Confirm Delete</h2>
          <p class="mt-4 text-gray-600">Are you sure you want to delete this user? This action cannot be undone.</p>
          
          <div class="flex justify-end mt-8 space-x-3">
            <button id="delete-cancel" class="btn-secondary">Cancel</button>
            <button id="delete-confirm" class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
  
  // Get users data
  try {
    const users = await userApi.getUsers();
    renderUsersList(users);
  } catch (error) {
    console.error('Error fetching users:', error);
    document.getElementById('users-list').innerHTML = `
      <div class="p-4 text-sm text-red-500">
        Error loading users: ${error.message || 'Unknown error'}
      </div>
    `;
  }

  // Add event listeners
  const newUserButton = document.getElementById('new-user-button');
  const modal = document.getElementById('user-modal');
  const backdrop = document.getElementById('modal-backdrop');
  const cancelButton = document.getElementById('cancel-button');
  const userForm = document.getElementById('user-form');
  const roleSelect = document.getElementById('user-role');
  const pinContainer = document.getElementById('pin-container');
  
  // Initialize delete modal events
  const deleteModal = document.getElementById('delete-modal');
  const deleteCancel = document.getElementById('delete-cancel');
  const deleteConfirm = document.getElementById('delete-confirm');
  
  // Show modal on new user button click
  newUserButton.addEventListener('click', () => {
    openUserModal();
  });
  
  // Hide modal on cancel or backdrop click
  cancelButton.addEventListener('click', closeUserModal);
  backdrop.addEventListener('click', closeUserModal);
  
  // Show/hide PIN field based on role selection
  roleSelect.addEventListener('change', () => {
    pinContainer.style.display = roleSelect.value === 'Operator' ? 'block' : 'none';
  });
  
  // Handle form submission
  userForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const saveButton = document.getElementById('save-button');
    const saveText = document.getElementById('save-button-text');
    const saveSpinner = document.getElementById('save-spinner');
    
    // Get form data
    const email = document.getElementById('user-email').value;
    const role = document.getElementById('user-role').value;
    const pin = document.getElementById('user-pin').value;
    const userId = userForm.dataset.userId;
    
    // Form data object
    const userData = {
      email,
      role
    };
    
    // Only include PIN if value is provided and role is Operator
    if (pin && role === 'Operator') {
      userData.pin = pin;
    }
    
    // Show loading state
    saveButton.disabled = true;
    saveText.textContent = userId ? 'Updating...' : 'Creating...';
    saveSpinner.classList.remove('hidden');
    
    try {
      if (userId) {
        await userApi.updateUser(userId, userData);
      } else {
        await userApi.createUser(userData);
      }
      
      // Close modal and refresh list
      closeUserModal();
      const users = await userApi.getUsers();
      renderUsersList(users);
    } catch (error) {
      alert(`Error: ${error.message || 'Unknown error occurred'}`);
      
      // Reset button state
      saveButton.disabled = false;
      saveText.textContent = userId ? 'Update' : 'Save';
      saveSpinner.classList.add('hidden');
    }
  });
  
  // Initialize delete modal handlers
  deleteCancel.addEventListener('click', () => {
    deleteModal.classList.add('hidden');
  });
  
  deleteConfirm.addEventListener('click', async () => {
    const userId = deleteConfirm.dataset.userId;
    if (!userId) return;
    
    try {
      await userApi.deleteUser(userId);
      deleteModal.classList.add('hidden');
      
      // Refresh the list
      const users = await userApi.getUsers();
      renderUsersList(users);
    } catch (error) {
      alert(`Error deleting user: ${error.message || 'Unknown error'}`);
    }
  });
}

// Helper function to render the users list
function renderUsersList(users = []) {
  const usersContainer = document.getElementById('users-list');
  
  if (!users.length) {
    usersContainer.innerHTML = `
      <div class="p-4 text-gray-500">
        No users found. Click "New User" to add one.
      </div>
    `;
    return;
  }
  
  usersContainer.innerHTML = `
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
            Email
          </th>
          <th scope="col" class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
            Role
          </th>
          <th scope="col" class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
            Created
          </th>
          <th scope="col" class="px-6 py-3 text-xs font-medium tracking-wider text-right text-gray-500 uppercase">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        ${users.map(user => `
          <tr>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">${user.email}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="inline-flex px-2 text-xs font-semibold leading-5 text-green-800 bg-green-100 rounded-full">
                ${user.role}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">${new Date(user.created_at).toLocaleDateString()}</div>
            </td>
            <td class="px-6 py-4 text-sm text-right whitespace-nowrap">
              <button data-user-id="${user.guid}" class="edit-user-btn text-primary-600 hover:text-primary-900">
                Edit
              </button>
              <button data-user-id="${user.guid}" class="ml-4 delete-user-btn text-red-600 hover:text-red-900">
                Delete
              </button>
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
  
  // Add event listeners to action buttons
  document.querySelectorAll('.edit-user-btn').forEach(button => {
    button.addEventListener('click', async () => {
      const userId = button.dataset.userId;
      try {
        const user = await userApi.getUser(userId);
        openUserModal(user);
      } catch (error) {
        alert(`Error loading user: ${error.message || 'Unknown error'}`);
      }
    });
  });
  
  document.querySelectorAll('.delete-user-btn').forEach(button => {
    button.addEventListener('click', () => {
      const userId = button.dataset.userId;
      const deleteModal = document.getElementById('delete-modal');
      const deleteConfirm = document.getElementById('delete-confirm');
      
      deleteConfirm.dataset.userId = userId;
      deleteModal.classList.remove('hidden');
    });
  });
}

// Helper to open the user modal
function openUserModal(user = null) {
  const modal = document.getElementById('user-modal');
  const form = document.getElementById('user-form');
  const title = document.getElementById('modal-title');
  const emailInput = document.getElementById('user-email');
  const roleSelect = document.getElementById('user-role');
  const pinInput = document.getElementById('user-pin');
  const pinContainer = document.getElementById('pin-container');
  const saveButton = document.getElementById('save-button-text');
  
  // Reset form
  form.reset();
  
  if (user) {
    // Edit mode
    title.textContent = 'Edit User';
    emailInput.value = user.email;
    roleSelect.value = user.role;
    pinInput.value = user.pin || '';
    form.dataset.userId = user.guid;
    saveButton.textContent = 'Update';
  } else {
    // Create mode
    title.textContent = 'Add New User';
    delete form.dataset.userId;
    saveButton.textContent = 'Save';
  }
  
  // Show/hide PIN field based on role
  pinContainer.style.display = roleSelect.value === 'Operator' ? 'block' : 'none';
  
  // Show modal
  modal.classList.remove('hidden');
}

// Helper to close the user modal
function closeUserModal() {
  const modal = document.getElementById('user-modal');
  modal.classList.add('hidden');
} 