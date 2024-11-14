// src/components/CreateProjectModal.js
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './ProjectModal.css';
import api from '../services/api';

function ProjectModal({ onClose, onProjectCreate }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [image_url, setImageUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await api.post('/projects', { title, description, image_url });
      onProjectCreate(response.data); // Pass the new project to parent
      setLoading(false);
      onClose(); // Close the modal
    } catch (err) {
      console.error("Error creating project:", err);
      setError(err.response?.data?.detail || "An error occurred while creating the project.");
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>Create New Project</h2>
        <form onSubmit={handleCreate} className="modal-form">
          <label>
            Title:
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              placeholder="Enter project title"
            />
          </label>
          <label>
            Description:
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter project description (optional)"
            />
          </label>
          <label>
            Image URL:
            <input
              type="url"
              value={image_url}
              onChange={(e) => setImageUrl(e.target.value)}
              placeholder="Enter image URL (optional)"
            />
          </label>
          {error && <p className="error">{error}</p>}
          <div className="modal-buttons">
            <button type="submit" disabled={loading}>
              {loading ? "Creating..." : "Create"}
            </button>
            <button type="button" onClick={onClose} className="cancel-button">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}

ProjectModal.propTypes = {
  onClose: PropTypes.func.isRequired,
  onProjectCreate: PropTypes.func.isRequired,
};

export default ProjectModal;
