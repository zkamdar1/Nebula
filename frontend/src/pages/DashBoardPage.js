// src/pages/DashboardPage.js
import React, { useState } from 'react';
import { auth } from '../services/firebase';
import { signOut } from 'firebase/auth';
import { FaUserCircle, FaPlus } from 'react-icons/fa'; // Account icon and plus icon
import './DashboardPage.css';

function DashboardPage() {
  const [showDropdown, setShowDropdown] = useState(false);
  const projects = []; // Replace with your array of project objects

  const handleLogout = async () => {
    await signOut(auth);
  };

  return (
    <div className="dashboard-container">
      {/* Account Icon and Dropdown */}
      <div className="account-icon" onClick={() => setShowDropdown(!showDropdown)}>
        <FaUserCircle size={30} />
        {showDropdown && (
          <div className="dropdown-menu">
            <p className="dropdown-item" onClick={handleLogout}>Sign Out</p>
          </div>
        )}
      </div>

      {/* New Project Card */}
      <div className="new-project-card">
        <FaPlus size={24} />
        <p>New Project</p>
      </div>

      {/* Existing Projects */}
      <div className="projects-container">
        {projects.length === 0 ? (
          <p className="no-projects">No projects yet</p>
        ) : (
          projects.map((project, index) => (
            <div key={index} className="project-card">
              <p>{project.name}</p>
              {/* Add more project details here as needed */}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default DashboardPage;
