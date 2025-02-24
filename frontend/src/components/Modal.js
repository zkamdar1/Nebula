// src/components/Modal.js
import React, { useState } from 'react';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../services/firebase";
import './Modal.css';
import api from '../services/api'; // Import API for backend communication

function Modal({ onClose, setUser }) {
  const [isRegister, setIsRegister] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleAuth = async (e) => {
    e.preventDefault();
    try {
      let firebaseUser;
      if (isRegister) {
        firebaseUser = await createUserWithEmailAndPassword(auth, email, password); 
      } else {
        firebaseUser = await signInWithEmailAndPassword(auth, email, password);
      }

      // Send the ID token and email to the appropriate backend endpoint
      const endpoint = isRegister ? '/auth/register' : '/auth/login';
      await api.post(endpoint, {
        email: firebaseUser.user.email,
      });
      
      // Set the authenticated Firebase user to the main state
      setUser(firebaseUser.user);
      onClose(); // Close the modal on successful authentication
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2 className="modal-title">{isRegister ? "Register" : "Login"}</h2>
        <form onSubmit={handleAuth} className="modal-form">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="modal-input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="modal-input"
          />
          {error && <p className="modal-error">{error}</p>}
          <button type="submit" className="modal-button">
            {isRegister ? "Register" : "Login"}
          </button>
        </form>
        <p className="modal-toggle" onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? "Already have an account? Login" : "Don't have an account? Register"}
        </p>
        <button className="modal-close-button" onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default Modal;
