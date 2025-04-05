import.meta.env = import.meta.env || {};

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:7770';
export const STATIC_URL = import.meta.env.VITE_STATIC_URL || 'http://localhost:7770';

export default {
    API_BASE_URL,
    STATIC_URL
};
