(function(){const r=document.createElement("link").relList;if(r&&r.supports&&r.supports("modulepreload"))return;for(const t of document.querySelectorAll('link[rel="modulepreload"]'))s(t);new MutationObserver(t=>{for(const o of t)if(o.type==="childList")for(const a of o.addedNodes)a.tagName==="LINK"&&a.rel==="modulepreload"&&s(a)}).observe(document,{childList:!0,subtree:!0});function n(t){const o={};return t.integrity&&(o.integrity=t.integrity),t.referrerPolicy&&(o.referrerPolicy=t.referrerPolicy),t.crossOrigin==="use-credentials"?o.credentials="include":t.crossOrigin==="anonymous"?o.credentials="omit":o.credentials="same-origin",o}function s(t){if(t.ep)return;t.ep=!0;const o=n(t);fetch(t.href,o)}})();const S=window.location.hostname==="localhost"||window.location.hostname==="127.0.0.1"?"http://localhost:8000/api/v1":"https://rafactory.raworkshop.bg/api/v1";function w(){const e=localStorage.getItem("auth");return e?JSON.parse(e):null}async function U(){const e=w();if(!e||!e.access_token)return!1;const r=new Date(e.expires_at);if(new Date>=r)try{return!!await A(e.refresh_token)}catch(s){return console.error("Error refreshing token:",s),L(),!1}return!0}async function H(e,r){try{const n=await fetch(`${S}/auth/login`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:e,password:r})});if(!n.ok){const a=await n.json();throw new Error(a.detail||"Login failed")}const s=await n.json(),t=new Date;t.setSeconds(t.getSeconds()+s.expires_in);const o={access_token:s.access_token,refresh_token:s.refresh_token,role:s.role,expires_at:t.toISOString()};return localStorage.setItem("auth",JSON.stringify(o)),o}catch(n){throw console.error("Login error:",n),n}}async function A(e){try{const r=await fetch(`${S}/auth/refresh`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({refresh_token:e})});if(!r.ok)throw new Error("Refresh token failed");const n=await r.json(),s=new Date;s.setSeconds(s.getSeconds()+n.expires_in);const t=w();return t.access_token=n.access_token,t.expires_at=s.toISOString(),localStorage.setItem("auth",JSON.stringify(t)),t}catch(r){throw console.error("Token refresh error:",r),L(),r}}function L(){localStorage.removeItem("auth"),window.location.href="/login"}function M(){const e=w();return e!=null&&e.access_token?{Authorization:`Bearer ${e.access_token}`}:{}}function D(e){e.innerHTML=`
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
  `;const r=document.getElementById("login-form"),n=document.getElementById("login-error"),s=document.getElementById("login-button-text"),t=document.getElementById("login-spinner");r.addEventListener("submit",async o=>{o.preventDefault();const a=document.getElementById("email").value,l=document.getElementById("password").value;s.textContent="Signing in...",t.classList.remove("hidden"),n.classList.add("hidden");try{await H(a,l),window.location.href="/"}catch(u){n.textContent=u.message||"Login failed. Please try again.",n.classList.remove("hidden"),s.textContent="Sign in",t.classList.add("hidden")}})}function $(){const e=w();return`
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
              <span class="mr-4 text-sm text-gray-600">${(e==null?void 0:e.role)||"Guest"}</span>
            </div>
            <button id="logout-button" class="px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-slate-100 hover:text-gray-900">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  `}const N=window.location.hostname==="localhost"||window.location.hostname==="127.0.0.1"?"http://localhost:8000/api/v1":"https://rafactory.raworkshop.bg/api/v1";async function T(e){if(e.ok)return e.status===204?null:await e.json();if(e.status===401)try{const n=localStorage.getItem("auth");if(n){const{refresh_token:s}=JSON.parse(n);await A(s);const t=e.url,o=e.method,a={"Content-Type":"application/json",...M()},l=await fetch(t,{method:o,headers:a});return T(l)}}catch(n){throw console.error("Failed to refresh token:",n),L(),new Error("Session expired. Please login again.")}const r=await e.json().catch(()=>({detail:"An unknown error occurred"}));throw new Error(r.detail||e.statusText)}async function m(e,r={}){const n=`${N}${e}`,s={"Content-Type":"application/json",...M(),...r.headers},t=await fetch(n,{...r,headers:s});return T(t)}const I={async getDashboardCounts(){var e,r,n,s,t,o,a,l;try{const[u,c,d,i]=await Promise.allSettled([m("/users?page=1&size=1"),m("/projects?page=1&size=1"),m("/workstations?page=1&size=1"),m("/companies")]);return{users:u.status==="fulfilled"&&(((e=u.value)==null?void 0:e.total_count)||((r=u.value)==null?void 0:r.length))||"?",projects:c.status==="fulfilled"&&(((n=c.value)==null?void 0:n.total_count)||((s=c.value)==null?void 0:s.length))||"?",workstations:d.status==="fulfilled"&&(((t=d.value)==null?void 0:t.total_count)||((o=d.value)==null?void 0:o.length))||"?",companies:i.status==="fulfilled"&&(((a=i.value)==null?void 0:a.total_count)||((l=i.value)==null?void 0:l.length))||"?"}}catch(u){return console.error("Error fetching dashboard counts:",u),{users:"?",projects:"?",workstations:"?",companies:"?"}}},async getCompanyInfo(){try{return await m("/companies/current")}catch(e){return console.error("Error fetching company info:",e),null}},async getRecentActivity(e=5){try{return m(`/activity?limit=${e}`)}catch(r){return console.error("Error fetching recent activity:",r),[]}}},v={async getUsers(e=1,r=10){return m(`/users?page=${e}&size=${r}`)},async getUser(e){return m(`/users/${e}`)},async createUser(e){return m("/users",{method:"POST",body:JSON.stringify(e)})},async updateUser(e,r){return m(`/users/${e}`,{method:"PATCH",body:JSON.stringify(r)})},async deleteUser(e){return m(`/users/${e}`,{method:"DELETE"})}},k={async getCompanies(e=1,r=10){try{return await m(`/companies?page=${e}&size=${r}`)}catch(n){if(console.error("Error fetching companies:",n),n.message.includes("Not Found")){const s=await this.getCurrentCompany();return s?[s]:[]}throw n}},async getCurrentCompany(){return m("/companies/current")},async getCompany(e){return m(`/companies/${e}`)},async createCompany(e){return m("/companies",{method:"POST",body:JSON.stringify(e)})},async updateCompany(e,r){return m(`/companies/${e}`,{method:"PATCH",body:JSON.stringify(r)})},async deleteCompany(e){return m(`/companies/${e}`,{method:"DELETE"})}};async function P(e){var r,n;w(),e.innerHTML=`
    <div class="min-h-screen bg-slate-100">
      ${$()}
      
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
  `;try{try{const t=await I.getCompanyInfo(),o=document.getElementById("company-info-container");t?o.innerHTML=`
          <div class="flex items-center">
            <div class="w-14 h-14 bg-primary-100 rounded-full flex items-center justify-center mr-4">
              <span class="text-xl font-bold text-primary-700">${((r=t.short_name)==null?void 0:r.substring(0,2))||((n=t.name)==null?void 0:n.substring(0,2))||"??"}</span>
            </div>
            <div>
              <h2 class="text-2xl font-semibold text-gray-800">${t.name||"Unknown Company"}</h2>
              <p class="text-gray-500">
                ${t.subscription_tier||"No"} Plan
                ${t.created_at?`· Since ${new Date(t.created_at).toLocaleDateString()}`:""}
              </p>
            </div>
            <div class="ml-auto">
              <span class="px-3 py-1 text-sm rounded-full 
                ${t.subscription_status==="active"?"bg-green-100 text-green-800":t.subscription_status==="trial"?"bg-yellow-100 text-yellow-800":"bg-red-100 text-red-800"}">
                ${t.subscription_status==="active"?"Active":t.subscription_status==="trial"?"Trial":"Inactive"}
              </span>
            </div>
          </div>
        `:o.innerHTML=`
          <div class="p-4 border border-gray-200 rounded-md">
            <p class="text-center text-gray-500">Company information not available</p>
          </div>
        `}catch(t){console.error("Error fetching company info:",t),document.getElementById("company-info-container").innerHTML=`
        <div class="p-4 border border-red-200 rounded-md">
          <p class="text-center text-red-500">Error loading company information</p>
        </div>
      `}const s=await I.getDashboardCounts();document.getElementById("users-count").textContent=s.users,document.getElementById("companies-count").textContent=s.companies,document.getElementById("projects-count").textContent=s.projects,document.getElementById("workstations-count").textContent=s.workstations;try{const t=await I.getRecentActivity(),o=document.getElementById("activity-container");t&&t.length>0?o.innerHTML=`
          <ul class="divide-y divide-gray-200">
            ${t.map(a=>{var l;return`
              <li class="py-3">
                <div class="flex items-start">
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center justify-center h-8 w-8 rounded-full bg-primary-100">
                      <span class="text-sm font-medium text-primary-800">${((l=a.user)==null?void 0:l.substring(0,1))||"?"}</span>
                    </span>
                  </div>
                  <div class="ml-4">
                    <p class="text-sm font-medium text-gray-900">${a.action||"Action"}</p>
                    <p class="text-sm text-gray-500">${a.details||""}</p>
                    <p class="mt-1 text-xs text-gray-400">${new Date(a.timestamp).toLocaleString()}</p>
                  </div>
                </div>
              </li>
            `}).join("")}
          </ul>
        `:o.innerHTML=`
          <p>No recent activity to display.</p>
        `}catch(t){console.error("Error rendering activity:",t),document.getElementById("activity-container").innerHTML=`
        <p>No recent activity to display.</p>
      `}try{const t=await v.getUsers(1,5),o=document.getElementById("users-list-container");t&&t.length>0?o.innerHTML=`
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
                ${t.map(a=>{var l;return`
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                          <span class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-primary-100">
                            <span class="font-medium text-primary-800">${((l=a.email)==null?void 0:l.substring(0,1).toUpperCase())||"?"}</span>
                          </span>
                        </div>
                        <div class="ml-4">
                          <div class="text-sm font-medium text-gray-900">${a.email||"Unknown Email"}</div>
                          <div class="text-sm text-gray-500">${a.guid||""}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-900">${a.role||"N/A"}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${a.is_active?"bg-green-100 text-green-800":"bg-red-100 text-red-800"}">
                        ${a.is_active?"Active":"Inactive"}
                      </span>
                    </td>
                  </tr>
                `}).join("")}
              </tbody>
            </table>
          </div>
        `:o.innerHTML=`
          <p class="text-center py-4">No users found.</p>
        `}catch(t){console.error("Error fetching users:",t),document.getElementById("users-list-container").innerHTML=`
        <p class="text-center py-4 text-red-600">Error loading users. Please try again.</p>
      `}}catch(s){console.error("Error rendering dashboard:",s),document.getElementById("company-info-container").innerHTML=`
      <div class="p-4 border border-red-200 rounded-md">
        <p class="text-center text-red-500">Error loading company information</p>
      </div>
    `,document.getElementById("users-count").textContent="?",document.getElementById("companies-count").textContent="?",document.getElementById("projects-count").textContent="?",document.getElementById("workstations-count").textContent="?",document.getElementById("activity-container").innerHTML=`
      <p>No recent activity to display.</p>
    `,document.getElementById("users-list-container").innerHTML=`
      <p class="text-center py-4">Unable to load users.</p>
    `}}const O=["CompanyAdmin","ProjectManager","Operator"];async function z(e){e.innerHTML=`
    <div class="min-h-screen bg-slate-100">
      ${$()}
      
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
                ${O.map(d=>`<option value="${d}">${d}</option>`).join("")}
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
  `;try{const d=await v.getUsers();C(d)}catch(d){console.error("Error fetching users:",d),document.getElementById("users-list").innerHTML=`
      <div class="p-4 text-sm text-red-500">
        Error loading users: ${d.message||"Unknown error"}
      </div>
    `}const r=document.getElementById("new-user-button");document.getElementById("user-modal");const n=document.getElementById("modal-backdrop"),s=document.getElementById("cancel-button"),t=document.getElementById("user-form"),o=document.getElementById("user-role"),a=document.getElementById("pin-container"),l=document.getElementById("delete-modal"),u=document.getElementById("delete-cancel"),c=document.getElementById("delete-confirm");r.addEventListener("click",()=>{_()}),s.addEventListener("click",B),n.addEventListener("click",B),o.addEventListener("change",()=>{a.style.display=o.value==="Operator"?"block":"none"}),t.addEventListener("submit",async d=>{d.preventDefault();const i=document.getElementById("save-button"),y=document.getElementById("save-button-text"),p=document.getElementById("save-spinner"),f=document.getElementById("user-email").value,x=document.getElementById("user-role").value,g=document.getElementById("user-pin").value,h=t.dataset.userId,b={email:f,role:x};g&&x==="Operator"&&(b.pin=g),i.disabled=!0,y.textContent=h?"Updating...":"Creating...",p.classList.remove("hidden");try{h?await v.updateUser(h,b):await v.createUser(b),B();const E=await v.getUsers();C(E)}catch(E){alert(`Error: ${E.message||"Unknown error occurred"}`),i.disabled=!1,y.textContent=h?"Update":"Save",p.classList.add("hidden")}}),u.addEventListener("click",()=>{l.classList.add("hidden")}),c.addEventListener("click",async()=>{const d=c.dataset.userId;if(d)try{await v.deleteUser(d),l.classList.add("hidden");const i=await v.getUsers();C(i)}catch(i){alert(`Error deleting user: ${i.message||"Unknown error"}`)}})}function C(e=[]){const r=document.getElementById("users-list");if(!e.length){r.innerHTML=`
      <div class="p-4 text-gray-500">
        No users found. Click "New User" to add one.
      </div>
    `;return}r.innerHTML=`
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
        ${e.map(n=>`
          <tr>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">${n.email}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="inline-flex px-2 text-xs font-semibold leading-5 text-green-800 bg-green-100 rounded-full">
                ${n.role}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">${new Date(n.created_at).toLocaleDateString()}</div>
            </td>
            <td class="px-6 py-4 text-sm text-right whitespace-nowrap">
              <button data-user-id="${n.guid}" class="edit-user-btn text-primary-600 hover:text-primary-900">
                Edit
              </button>
              <button data-user-id="${n.guid}" class="ml-4 delete-user-btn text-red-600 hover:text-red-900">
                Delete
              </button>
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `,document.querySelectorAll(".edit-user-btn").forEach(n=>{n.addEventListener("click",async()=>{const s=n.dataset.userId;try{const t=await v.getUser(s);_(t)}catch(t){alert(`Error loading user: ${t.message||"Unknown error"}`)}})}),document.querySelectorAll(".delete-user-btn").forEach(n=>{n.addEventListener("click",()=>{const s=n.dataset.userId,t=document.getElementById("delete-modal"),o=document.getElementById("delete-confirm");o.dataset.userId=s,t.classList.remove("hidden")})})}function _(e=null){const r=document.getElementById("user-modal"),n=document.getElementById("user-form"),s=document.getElementById("modal-title"),t=document.getElementById("user-email"),o=document.getElementById("user-role"),a=document.getElementById("user-pin"),l=document.getElementById("pin-container"),u=document.getElementById("save-button-text");n.reset(),e?(s.textContent="Edit User",t.value=e.email,o.value=e.role,a.value=e.pin||"",n.dataset.userId=e.guid,u.textContent="Update"):(s.textContent="Add New User",delete n.dataset.userId,u.textContent="Save"),l.style.display=o.value==="Operator"?"block":"none",r.classList.remove("hidden")}function B(){document.getElementById("user-modal").classList.add("hidden")}async function R(e){var u;w(),e.innerHTML=`
    <div class="min-h-screen bg-slate-100">
      ${$()}
      
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
  `;try{const c=await k.getCompanies(),d=document.getElementById("companies-list");c&&c.length>0?d.innerHTML=`
        <ul class="divide-y divide-gray-200">
          ${c.map(i=>{var y,p;return`
            <li class="p-4 hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-12 w-12 bg-primary-100 rounded-full flex items-center justify-center">
                    <span class="text-lg font-semibold text-primary-800">${((y=i.short_name)==null?void 0:y.substring(0,2))||((p=i.name)==null?void 0:p.substring(0,2))||"??"}</span>
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-medium text-gray-900">${i.name}</h3>
                    <div class="flex items-center text-sm text-gray-500">
                      <span class="mr-2">${i.subscription_tier||"No"} Plan</span>
                      <span class="px-2 py-0.5 text-xs rounded-full 
                        ${i.subscription_status==="active"?"bg-green-100 text-green-800":i.subscription_status==="trial"?"bg-yellow-100 text-yellow-800":"bg-red-100 text-red-800"}">
                        ${i.subscription_status==="active"?"Active":i.subscription_status==="trial"?"Trial":"Inactive"}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="flex space-x-2">
                  <button class="edit-company-btn p-1 text-gray-400 hover:text-primary-600" data-id="${i.guid}">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button class="delete-company-btn p-1 text-gray-400 hover:text-red-600" data-id="${i.guid}">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </li>
          `}).join("")}
        </ul>
      `:(d.innerHTML=`
        <div class="p-6 text-center">
          <p class="text-gray-500">No companies found</p>
          <button id="no-companies-add-btn" class="mt-2 inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-600 border border-primary-300 rounded-md hover:bg-primary-50">
            <svg class="mr-1 -ml-0.5 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Add Your First Company
          </button>
        </div>
      `,(u=document.getElementById("no-companies-add-btn"))==null||u.addEventListener("click",()=>n())),r(c)}catch(c){console.error("Error rendering companies page:",c),document.getElementById("companies-list").innerHTML=`
      <div class="p-6 text-center">
        <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <p class="mt-2 text-gray-500">Error loading companies</p>
      </div>
    `}function r(c){var d,i,y,p,f,x;(d=document.getElementById("add-company-btn"))==null||d.addEventListener("click",()=>n()),document.querySelectorAll(".edit-company-btn").forEach(g=>{g.addEventListener("click",async()=>{const h=g.getAttribute("data-id"),b=c.find(E=>E.guid===h);b&&n(b)})}),document.querySelectorAll(".delete-company-btn").forEach(g=>{g.addEventListener("click",()=>{const h=g.getAttribute("data-id");t(h)})}),(i=document.getElementById("close-modal-btn"))==null||i.addEventListener("click",s),(y=document.getElementById("cancel-btn"))==null||y.addEventListener("click",s),(p=document.getElementById("cancel-delete-btn"))==null||p.addEventListener("click",o),(f=document.getElementById("company-form"))==null||f.addEventListener("submit",a),(x=document.getElementById("confirm-delete-btn"))==null||x.addEventListener("click",l)}function n(c=null){const d=document.getElementById("company-modal"),i=document.getElementById("modal-title"),y=document.getElementById("company-form"),p=document.getElementById("company-id"),f=document.getElementById("company-name"),x=document.getElementById("company-short-name"),g=document.getElementById("subscription-tier"),h=document.getElementById("subscription-status");y.reset(),c?(i.textContent="Edit Company",p.value=c.guid,f.value=c.name||"",x.value=c.short_name||"",g.value=c.subscription_tier||"Basic",h.value=c.subscription_status||"active"):(i.textContent="Add Company",p.value=""),d.classList.remove("hidden")}function s(){document.getElementById("company-modal").classList.add("hidden")}function t(c){document.getElementById("delete-confirm-modal").classList.remove("hidden"),document.getElementById("confirm-delete-btn").setAttribute("data-id",c)}function o(){document.getElementById("delete-confirm-modal").classList.add("hidden")}async function a(c){c.preventDefault();const d=document.getElementById("company-id"),i=document.getElementById("company-name"),y=document.getElementById("company-short-name"),p=document.getElementById("subscription-tier"),f=document.getElementById("subscription-status"),x={name:i.value.trim(),short_name:y.value.trim(),subscription_tier:p.value,subscription_status:f.value};try{d.value?await k.updateCompany(d.value,x):await k.createCompany(x),window.location.reload()}catch(g){console.error("Error saving company:",g),alert("Failed to save company. Please try again.")}}async function l(){const d=document.getElementById("confirm-delete-btn").getAttribute("data-id");if(d)try{await k.deleteCompany(d),window.location.reload()}catch(i){console.error("Error deleting company:",i),alert("Failed to delete company. Please try again."),o()}}}const j={"/":P,"/login":D,"/users":z,"/companies":R};function q(){const e=document.getElementById("app");async function r(s){const t=j[s]||j["/"];if(t.constructor.name==="AsyncFunction")try{await t(e)}catch(o){console.error("Error rendering page:",o),e.innerHTML=`
          <div class="flex items-center justify-center min-h-screen">
            <div class="p-6 bg-white rounded-lg shadow-md">
              <h2 class="text-xl font-semibold text-red-600">Error Loading Page</h2>
              <p class="mt-2 text-gray-600">There was an error loading this page. Please try again.</p>
              <button onclick="window.location.reload()" class="px-4 py-2 mt-4 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700">
                Reload
              </button>
            </div>
          </div>
        `}else t(e)}const n=window.location.pathname||"/";r(n),document.addEventListener("click",s=>{var o;const t=s.target.closest("a");if(t&&((o=t.getAttribute("href"))!=null&&o.startsWith("/"))){s.preventDefault();const a=t.getAttribute("href");window.history.pushState({},"",a),r(a)}}),window.addEventListener("popstate",()=>{const s=window.location.pathname;r(s)})}document.addEventListener("DOMContentLoaded",async()=>{if(!await U()&&window.location.pathname!=="/login"){window.location.href="/login";return}q()});
