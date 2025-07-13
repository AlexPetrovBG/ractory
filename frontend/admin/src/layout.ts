// src/layout.ts

// Declare global Metronic components on window
declare global {
  interface Window {
    KTApp?: any;
    KTMenu?: any;
    KTToggle?: any;
    KTDrawer?: any;
    KTScroll?: any;
  }
}

// Function to render the main application layout HTML structure
// This HTML is adapted from Metronic Tailwind Demo10
const renderLayout = (): string => {
  return `
    <div class="grid grid-cols-[auto_1fr] h-full overflow-hidden mx-auto w-full" id="kt_app_root">
      <!-- Sidebar -->
      <div class="bg-white dark:bg-coal-600 shadow-sm min-w-[300px] w-[300px] transition-all duration-300 ease-in-out" id="kt_app_sidebar">
        ${renderSidebar()}
      </div>

      <!-- Main Content Area -->
      <div class="flex flex-col h-full" id="kt_app_main">
        <!-- Header -->
        <div class="bg-white dark:bg-coal-700 z-20 shadow sticky top-0" id="kt_app_header">
          ${renderHeader()}
        </div>

        <!-- Content -->
        <div class="grow overflow-auto p-6 bg-gray-50 dark:bg-coal-500" id="kt_app_content">
          <div class="mx-auto" id="kt_app_content_container">
            <!-- Page content goes here -->
          </div>
        </div>

        <!-- Footer -->
        <div class="bg-white dark:bg-coal-700 py-4 px-6 shadow-inner" id="kt_app_footer">
          ${renderFooter()}
        </div>
      </div>
    </div>
    
    <!-- Scroll to top -->
    <div class="hidden" id="kt_scrolltop">
      <div class="scrolltop w-10 h-10 rounded-full bg-primary flex items-center justify-center fixed bottom-5 end-5 cursor-pointer shadow-sm z-50">
        <span class="ki-duotone ki-arrow-up-circle text-white">
          <i class="path1"></i>
          <i class="path2"></i>
        </span>
      </div>
    </div>
  `;
};

// Render header with Tailwind classes
const renderHeader = (): string => `
  <div class="flex items-center justify-between px-6 py-4">
    <div class="flex items-center">
      <!-- Mobile toggle button -->
      <button class="lg:hidden btn btn-icon btn-sm" id="kt_app_sidebar_toggle">
        <i class="ki-duotone ki-abstract-13 fs-1">
          <i class="path1"></i>
          <i class="path2"></i>
        </i>
      </button>
      <!-- Page title -->
      <h1 class="text-gray-900 dark:text-white text-xl font-bold ms-4">Dashboard</h1>
    </div>
    <!-- Header actions -->
    <div class="flex items-center gap-3">
      <!-- User menu -->
      <div class="relative" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">
        <button class="btn btn-sm px-3 btn-light">
          <div class="flex items-center">
            <div class="symbol symbol-30px me-3">
              <img alt="User" src="/assets/media/avatars/300-1.jpg" />
            </div>
            <span class="text-gray-800 dark:text-white font-medium">Admin</span>
            <i class="ki-duotone ki-down fs-3 ms-2"></i>
          </div>
        </button>
        <!-- User menu dropdown -->
        <div class="menu menu-sub menu-sub-dropdown menu-column py-3 px-3 w-200px hidden" data-kt-menu="true">
          <div class="menu-item">
            <a href="#" class="menu-link px-3 py-2" onclick="localStorage.removeItem('access_token'); window.location.reload();">Sign Out</a>
          </div>
        </div>
      </div>
    </div>
  </div>
`;

// Render sidebar with Tailwind classes
const renderSidebar = (): string => `
  <!-- Sidebar header / logo -->
  <div class="flex items-center justify-between py-5 px-6 border-b border-gray-200 dark:border-coal-500">
    <a href="#" class="flex items-center">
      <img alt="Logo" src="/assets/media/brand-logos/logo.svg" class="h-7 me-3" />
      <span class="text-gray-900 dark:text-white text-lg font-bold">RaFactory</span>
    </a>
  </div>
  
  <!-- Sidebar menu -->
  <div class="overflow-y-auto h-[calc(100vh-70px)]" id="kt_app_sidebar_menu">
    <ul class="menu py-3">
      <li class="menu-item">
        <a href="#/dashboard" class="menu-link active px-6 py-4 flex items-center gap-3">
          <i class="ki-duotone ki-element-11 text-primary fs-2">
            <i class="path1"></i>
            <i class="path2"></i>
            <i class="path3"></i>
            <i class="path4"></i>
          </i>
          <span class="text-gray-800 dark:text-white">Dashboard</span>
        </a>
      </li>
      <li class="menu-item">
        <a href="#/users" class="menu-link px-6 py-4 flex items-center gap-3">
          <i class="ki-duotone ki-people fs-2">
            <i class="path1"></i>
            <i class="path2"></i>
            <i class="path3"></i>
            <i class="path4"></i>
            <i class="path5"></i>
          </i>
          <span class="text-gray-800 dark:text-white">Users</span>
        </a>
      </li>
      <!-- Add more menu items as needed -->
    </ul>
  </div>
`;

// Render toolbar with Tailwind classes
const renderToolbar = (): string => `
  <div class="flex flex-wrap items-center justify-between mb-4">
    <h2 class="text-gray-900 dark:text-white text-xl font-bold">Page Title</h2>
    <div class="flex items-center gap-2">
      <!-- Toolbar actions -->
    </div>
  </div>
`;

// Render footer with Tailwind classes
const renderFooter = (): string => `
  <div class="flex flex-col md:flex-row justify-between items-center">
    <div class="text-sm text-gray-600 dark:text-gray-300">
      <span class="text-gray-700 dark:text-gray-200 font-bold">RaFactory</span> &copy; 2025
    </div>
    <div class="flex gap-3 mt-3 md:mt-0">
      <a href="#" class="text-sm text-gray-600 dark:text-gray-300 hover:text-primary">About</a>
      <a href="#" class="text-sm text-gray-600 dark:text-gray-300 hover:text-primary">Support</a>
    </div>
  </div>
`;

// Function to initialize Metronic components after layout is rendered
export const initializeLayout = (appElement: HTMLElement) => {
  appElement.innerHTML = renderLayout();

  // Initialize Metronic components that rely on the DOM structure
  if (window.KTApp) {
    window.KTApp.init(); // General layout
  }
  if (window.KTMenu) {
    window.KTMenu.createInstances('[data-kt-menu="true"]');
  }
  if (window.KTToggle) {
    window.KTToggle.createInstances(); // For sidebar toggles, etc.
  }
  if (window.KTDrawer) {
    window.KTDrawer.createInstances();
  }
};

// Function to load content into the main content area
export const loadContent = (htmlContent: string) => {
  const container = document.getElementById('kt_app_content_container');
  if (container) {
    container.innerHTML = htmlContent;
    // Potentially initialize Metronic components specific to the loaded content here
  } else {
    console.error("Content container 'kt_app_content_container' not found.");
  }
}; 