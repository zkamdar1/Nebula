// src/pages/DashboardPage.js
import React, { useState, useEffect } from 'react';
import { auth } from '../services/firebase';
import { signOut } from 'firebase/auth';
import { FaUserCircle, FaPlus } from 'react-icons/fa'; // Account icon and plus icon
import './DashboardPage.css';
import ProjectCard from '../components/ProjectCard';
import api from '../services/api';

function DashboardPage() {
  const [projects, setProjects] = useState([]);
  const [showModal, setShowModal] = useState(false);

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

  const createProject = async () => {
    const title = prompt("Enter project title:");
    const description = prompt("Enter project description:");
    if (title && description) {
      try {
        const response = await api.post('/projects', { title, description });
        setProjects([...projects, response.data]);
      } catch (error) {
        console.error("Error creating project:", error);
      }
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
          projects.map((project) => (
            <ProjectCard
              key={project.id}
              title={project.title}
              description={project.description}
              lastAccessed={project.last_accessed} />
          ))
        )}
      </div>
    </div>
  );
}

export default DashboardPage;
