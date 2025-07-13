export interface ApiClient {
    get: <T = any>(path: string, params?: Record<string, any>) => Promise<T>;
    post: <T = any>(path: string, data: any) => Promise<T>;
    patch: <T = any>(path: string, data: any) => Promise<T>;
    put: <T = any>(path: string, data: any) => Promise<T>;
    delete: <T = any>(path: string) => Promise<T>;
}

export const createApiClient = (baseURL: string = 'https://rafactory.raworkshop.bg/api/v1'): ApiClient => {
    const getAuthHeader = (): Record<string, string> => {
        const token = localStorage.getItem('access_token');
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    };

    const handleResponse = async (response: Response): Promise<any> => {
        if (!response.ok) {
            // Attempt to parse error JSON, otherwise throw status text
            let errorData;
            try {
                errorData = await response.json();
            } catch(e) {
                errorData = { message: response.statusText };
            }
            const error = new Error(errorData?.error?.message || response.statusText) as any;
            error.status = response.status;
            error.data = errorData; // Attach full error data if available
            throw error;
        }
        // Handle empty responses (e.g., 204 No Content)
        if (response.status === 204) {
            return null;
        }
        return response.json(); // Assume JSON response for success
    };

    const request = async (method: string, path: string, data?: any, params?: Record<string, any>): Promise<any> => {
        const url = new URL(path, baseURL);
        if (params) {
            Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
        }

        const options: RequestInit = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                ...getAuthHeader(),
            },
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url.toString(), options);
        return handleResponse(response);
    };

    return {
        get: <T = any>(path: string, params?: Record<string, any>) => request('GET', path, undefined, params) as Promise<T>,
        post: <T = any>(path: string, data: any) => request('POST', path, data) as Promise<T>,
        patch: <T = any>(path: string, data: any) => request('PATCH', path, data) as Promise<T>,
        put: <T = any>(path: string, data: any) => request('PUT', path, data) as Promise<T>,
        delete: <T = any>(path: string) => request('DELETE', path) as Promise<T>,
    };
}; 