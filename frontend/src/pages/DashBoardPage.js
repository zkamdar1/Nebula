// src/pages/DashboardPage.js
import React, { useState, useEffect } from 'react';
import { auth } from '../services/firebase';
import { signOut } from 'firebase/auth';
import { FaUserCircle, FaPlus, FaTimes } from 'react-icons/fa'; // Account icon and plus icon
import './DashboardPage.css';
import ProjectCard from '../components/ProjectCard';
import api from '../services/api';
import ProjectModal from '../components/ProjectModal'; // New Modal Component
import EditProjectModal from '../components/EditProjectModal';
import { updateEmail, updatePassword, deleteUser } from 'firebase/auth';

function DashboardPage() {
  const [projects, setProjects] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false); // State for Modal
  const [showSettings, setShowSettings] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editProject, setEditProject] = useState(null);

  const handleEditProject = (project) => {
    setEditProject(project);
    setShowEditModal(true);
  };

  const handleCloseModal = () => {
    setEditProject(null);
    setShowEditModal(false);
  };

  const handleProjectUpdate = (updatedProject) => {
    setProjects(projects.map(p => (p.id === updatedProject.id ? updatedProject : p)));
    handleCloseModal();
  };

  const handleDeleteProject = async (projectId) => {
    await api.delete(`/projects/${projectId}`);
    setProjects(projects.filter(p => p.id !== projectId));
    handleCloseModal();
  };

  const handleLogout = async () => {
    await signOut(auth);
  };

  const handleShowSettings = () => {
    setShowSettings(!showSettings);
  };
  
  const handleChangeEmail = async (newEmail) => {
    try {
      await updateEmail(auth.currentUser, newEmail);
      alert('Email updated successfully.');
    } catch (error) {
      console.error('Error updating email:', error.message);
      alert('Please reauthenticate to update your email.');
    }
  };

  const handleChangePassword = async (newPassword) => {
    try {
      await updatePassword(auth.currentUser, newPassword);
      alert('Password updated successfully.');
    } catch (error) {
      console.error('Error updating password:', error.message);
      alert('Please reauthenticate to update your password.');
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await deleteUser(auth.currentUser);
      alert('Account deleted successfully.');
    } catch (error) {
      console.error('Error deleting account:', error.message);
      alert('Please reauthenticate to delete your account.');
    }
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

  return (
    <div className="dashboard-container">
      {/* Account Icon and Dropdown */}
      <div className="account-icon" onClick={() => setShowDropdown(!showDropdown)}>
        <FaUserCircle size={30} />
        {showDropdown && (
          <div className="dropdown-menu">
            <p className="dropdown-item" onClick={handleLogout}>Sign Out</p>
            <p className="dropdown-item" onClick={handleShowSettings}>Settings</p>
          </div>
        )}
      </div>

      {showSettings && (
        <div className="settings-menu">
          <FaTimes className="close-icon" onClick={handleShowSettings} />
          <h3>Account Settings</h3>
          <input
            type="email"
            placeholder="New Email"
            onBlur={(e) => handleChangeEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="New Password"
            onBlur={(e) => handleChangePassword(e.target.value)}
          />
          <button onClick={handleDeleteAccount}>Delete Account</button>
        </div>
      )}

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
              lastAccessed={project.last_accessed}
              onEdit={() => handleEditProject(project)}/>
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
      {showEditModal && (
        <EditProjectModal
          project={editProject}
          onClose={handleCloseModal}
          onProjectUpdate={handleProjectUpdate}
          onDelete={() => handleDeleteProject(editProject.id)}
        />
      )}
    </div>
  );
}

export default DashboardPage;
