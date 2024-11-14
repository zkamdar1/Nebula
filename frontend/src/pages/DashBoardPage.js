// src/pages/DashboardPage.js
import React, { useState, useEffect } from 'react';
import { auth } from '../services/firebase';
import { signOut } from 'firebase/auth';
import { FaUserCircle, FaPlus } from 'react-icons/fa'; // Account icon and plus icon
import './DashboardPage.css';
import ProjectCard from '../components/ProjectCard';
import api from '../services/api';
import ProjectModal from '../components/ProjectModal'; // New Modal Component
import { getIdToken } from 'firebase/auth';

function DashboardPage() {
  const [projects, setProjects] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false); // State for Modal
  const [token, setToken] = useState('');
  
  const handleLogout = async () => {
    await signOut(auth);
  };

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects');
      setProjects(response.data);
    } catch (error) {
      console.error("Error fetching projects:", error);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleProjectCreate = (newProject) => {
    setProjects([newProject, ...projects]); // Add the new project to the beginning
  };

  const fetchToken = async () => {
    const user = auth.currentUser;
    if (user) {
      try {
        const idToken = await getIdToken(user);
        setToken(idToken);
        navigator.clipboard.writeText(idToken); // Optional: Copy to clipboard
        alert("Token copied to clipboard!");
      } catch (error) {
        console.error("Error fetching ID token:", error);
        alert("Failed to fetch token.");
      }
    } else {
      alert("No user is logged in.");
    }
  };

  return (
    <div className="dashboard-container">
      {/* Account Icon and Dropdown */}
      <div className="account-icon" onClick={() => setShowDropdown(!showDropdown)}>
        <FaUserCircle size={30} />
        {showDropdown && (
          <div className="dropdown-menu">
            <p className="dropdown-item" onClick={handleLogout}>Sign Out</p>
            <div>
              <button onClick={fetchToken}>Get Bearer Token</button>
                {token && (
                  <div>
                    <p>Your Bearer Token:</p>
                    <textarea readOnly value={token} rows="4" cols="50" />
                  </div>
                )}
            </div>
          </div>
        )}
      </div>

      {/* New Project Card */}
      <div className="new-project-card" onClick={() => setShowCreateModal(true)}>
        <FaPlus size={24} />
        <p>New Project</p>
      </div>

      {/* Existing Projects */}
      <div className="projects-container">
        {projects.length === 0 ? (
          <p className="no-projects">No projects yet</p>
        ) : (
          projects.map((project) => (
            <ProjectCard
              key={project.id}
              title={project.title}
              description={project.description}
              lastAccessed={project.last_accessed} />
          ))
        )}
      </div>
      {/* Create Project Modal */}
      {showCreateModal && (
        <ProjectModal
          onClose={() => setShowCreateModal(false)}
          onProjectCreate={handleProjectCreate}
        />
      )}
    </div>
  );
}

export default DashboardPage;
