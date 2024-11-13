import axios from 'axios';
import { auth } from './firebase'; // Ensure correct path
import { getIdToken } from 'firebase/auth';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Adjust if your backend is hosted elsewhere
});

// Add an interceptor to include the Firebase token in each request
api.interceptors.request.use(async (config) => {
  const token = await getFirebaseToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Function to retrieve the current user's ID token
const getFirebaseToken = async () => {
  const user = auth.currentUser;
  return user ? await getIdToken(user) : null;
};

export default api;
