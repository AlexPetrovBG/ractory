import { createApiClient } from './api'; // Import your API client creator
import type { ApiClient } from './api'; // Import the type if needed

// Declare global Metronic components on window
declare global {
  interface Window {
    KTTogglePassword?: any;
  }
}

const apiClient = createApiClient();

// Function to render the login page HTML
// Adapted from Demo10 Corporate sign-in template
const renderLoginPage = (): string => {
  return `
    <div class="flex items-center justify-center grow bg-center bg-no-repeat" style="background-image: url('/assets/media/images/2600x1200/bg-10.png');">
      <div class="card max-w-[370px] w-full">
        <form action="#" class="card-body flex flex-col gap-5 p-10" id="kt_sign_in_form" method="get">
          <div class="text-center mb-2.5">
            <h3 class="text-lg font-medium text-gray-900 leading-none mb-2.5">
              Sign in
            </h3>
            <div class="flex items-center justify-center font-medium">
              <span class="text-2sm text-gray-700 me-1.5">
                Need an account?
              </span>
              <a class="text-2sm link" href="#">
                Sign up
              </a>
            </div>
          </div>
          
          <!-- Social Login Buttons -->
          <div class="grid grid-cols-2 gap-2.5">
            <a class="btn btn-light btn-sm justify-center" href="#">
              <img alt="" class="size-3.5 shrink-0" src="/assets/media/brand-logos/google.svg"/>
              Use Google
            </a>
            <a class="btn btn-light btn-sm justify-center" href="#">
              <img alt="" class="size-3.5 shrink-0 dark:hidden" src="/assets/media/brand-logos/apple-black.svg"/>
              <img alt="" class="size-3.5 shrink-0 light:hidden" src="/assets/media/brand-logos/apple-white.svg"/>
              Use Apple
            </a>
          </div>
          
          <!-- Divider -->
          <div class="flex items-center gap-2">
            <span class="border-t border-gray-200 w-full"></span>
            <span class="text-2xs text-gray-500 font-medium uppercase">Or</span>
            <span class="border-t border-gray-200 w-full"></span>
          </div>
          
          <div class="flex flex-col gap-1">
            <label class="form-label font-normal text-gray-900">
              Email
            </label>
            <input class="input" name="email" placeholder="email@email.com" type="text" autocomplete="off" required />
          </div>
          
          <div class="flex flex-col gap-1">
            <div class="flex items-center justify-between gap-1">
              <label class="form-label font-normal text-gray-900">
                Password
              </label>
              <a class="text-2sm link shrink-0" href="#">
                Forgot Password?
              </a>
            </div>
            <div class="input" data-toggle-password="true">
              <input name="password" placeholder="Enter Password" type="password" autocomplete="off" required />
              <button class="btn btn-icon" data-toggle-password-trigger="true" type="button">
                <i class="ki-filled ki-eye text-gray-500 toggle-password-active:hidden"></i>
                <i class="ki-filled ki-eye-slash text-gray-500 hidden toggle-password-active:block"></i>
              </button>
            </div>
          </div>
          
          <label class="checkbox-group">
            <input class="checkbox checkbox-sm" name="remember" type="checkbox" value="1" />
            <span class="checkbox-label">
              Remember me
            </span>
          </label>
          
          <button type="submit" id="kt_sign_in_submit" class="btn btn-primary flex justify-center">
            <span class="indicator-label">Sign In</span>
            <span class="indicator-progress hidden">
              Please wait... <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
          </button>

          <!-- Error Message Placeholder -->
          <div id="kt_login_error_message" class="text-danger text-center hidden">
            Invalid credentials. Please try again.
          </div>
        </form>
      </div>
    </div>
  `;
};

// Function to display the login page
export const showLoginPage = (appElement: HTMLElement, loginHandler: (formData: any) => Promise<void>) => {
    appElement.innerHTML = renderLoginPage();

    const form = document.getElementById('kt_sign_in_form') as HTMLFormElement;
    const submitButton = document.getElementById('kt_sign_in_submit') as HTMLButtonElement;
    const errorMessage = document.getElementById('kt_login_error_message') as HTMLElement;
    const indicatorLabel = submitButton?.querySelector('.indicator-label') as HTMLElement;
    const indicatorProgress = submitButton?.querySelector('.indicator-progress') as HTMLElement;

    // Initialize toggle password
    const togglePassword = document.querySelector('[data-toggle-password="true"]');
    if (togglePassword && window.KTTogglePassword) {
        new window.KTTogglePassword(togglePassword);
    }

    if (form && submitButton && errorMessage) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            errorMessage.classList.add('hidden'); // Hide error initially

            // Show loading indicator
            if (indicatorLabel && indicatorProgress) {
                indicatorLabel.classList.add('hidden');
                indicatorProgress.classList.remove('hidden');
            }
            submitButton.disabled = true;

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                await loginHandler(data);
                // Success handled by redirection in main.ts/initApp
            } catch (error) {
                console.error('Login failed:', error);
                errorMessage.classList.remove('hidden'); // Show error
                
                // Hide loading indicator
                if (indicatorLabel && indicatorProgress) {
                    indicatorLabel.classList.remove('hidden');
                    indicatorProgress.classList.add('hidden');
                }
                submitButton.disabled = false;
            }
        });
    } else {
        console.error("Login form elements not found!");
    }
};

// Function to handle the actual login API call
export const handleLogin = async (credentials: any) => {
    try {
        const response = await apiClient.post('/auth/login', credentials);
        const { access_token, refresh_token /* other data */ } = response; // Adjust based on actual API response

        if (!access_token) {
            throw new Error("Access token not received");
        }

        // Store tokens securely (localStorage is simple, but consider HttpOnly cookies for refresh_token)
        localStorage.setItem('access_token', access_token);
        if (refresh_token) {
            // Handle refresh token storage (e.g., secure cookie or memory)
            localStorage.setItem('refresh_token', refresh_token);
        }

        // IMPORTANT: Reload the app or trigger re-initialization to load the main layout
        window.location.reload(); // Simple way to re-run initApp

    } catch (error) {
        console.error("API Login error:", error);
        // Re-throw the error so showLoginPage can handle UI feedback
        throw error;
    }
}; 