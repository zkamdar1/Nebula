// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Modal from './components/Modal';

function App() {
  const [showModal, setShowModal] = useState(false);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage setShowModal={setShowModal} />} />
      </Routes>
      {showModal && <Modal onClose={() => setShowModal(false)} />}
    </Router>
  );
}

export default App;
