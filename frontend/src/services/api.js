import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Adjust if your backend is hosted elsewhere
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

const getFirebaseToken = async () => {
  const user = await import('../services/firebase').then((firebase) => firebase.auth().currentUser);
  return user ? await user.getIdToken() : null;
};

export default api;
