// src/pages/LandingPage.js
import React, { useState } from 'react';
import { auth } from '../services/firebase';
import { signOut } from 'firebase/auth';
import { Link } from 'react-router-dom';
import Modal from '../components/Modal';
import './LandingPage.css';

function LandingPage({ user, setUser }) {
  const [showModal, setShowModal] = useState(false);

  const handleLogout = async () => {
    await signOut(auth);
    setUser(null);
  };

  return (
    <div className="landing-container">
      {user ? (
        <Link to="/dashboard" className="title-link">
          <h1 className="title-link">NEBULA</h1>
        </Link>
      ) : (
        <h1 className="title">NEBULA</h1>
      )}
      <p className="subtitle">Your one-stop short-form video generator.</p>

      {user ? (
        <button className="signout-button" onClick={handleLogout}>Sign Out</button>
      ) : (
        <button className="login-button" onClick={() => setShowModal(true)}>
          Login / Register
        </button>
      )}

      {showModal && <Modal onClose={() => setShowModal(false)} />}
    </div>
  );
}

export default LandingPage;
