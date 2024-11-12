// src/pages/LandingPage.js
import React, { useState } from 'react';
import Modal from '../components/Modal';
import './LandingPage.css';

function LandingPage() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="landing-container">
      <h1 className="title">NEBULA</h1>
      <p className="subtitle">Your one-stop short-form video generator.</p>
      <button className="login-button" onClick={() => setShowModal(true)}>
        Login / Register
      </button>
      {showModal && <Modal onClose={() => setShowModal(false)} />}
    </div>
  );
}

export default LandingPage;
