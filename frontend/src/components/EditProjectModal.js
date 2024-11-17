// src/components/CreateProjectModal.js
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './ProjectModal.css';
import api from '../services/api';

function EditProjectModal({  project, onClose, refreshProjects }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [image_url, setImageUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (project) {
      setTitle(project.title);
      setDescription(project.description);
      setImageUrl(project.imageUrl || '');
    }
  }, [project]);

  const handleEdit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await api.put(`/projects/${project.id}`, { title, description, image_url });
      refreshProjects(); // Pass the new project to parent
      setLoading(false);
      onClose(); // Close the modal
    } catch (err) {
      console.error("Error updating project:", err);
      setError(err.response?.data?.detail || "An error occurred while creating the project.");
      setLoading(false);
    }
  };

  // Delete project
  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this project?')) {
      return;
    }

    try {
      await api.delete(`/projects/${project.id}`);
      refreshProjects(); // Refresh projects in the parent component
      onClose(); // Close the modal
    } catch (err) {
      console.error('Error deleting project:', err);
      setError(err.response?.data?.detail || 'An error occurred while deleting the project.');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>Edit Project</h2>
        <form onSubmit={handleEdit} className="modal-form">
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
            Edit Description:
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter project description (optional)"
            />
          </label>
          <label>
            Change Image URL:
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
              {loading ? "Updating..." : "Update"}
            </button>
            <button type="button" onClick={handleDelete}
              className="delete-button"
            >Delete</button>
            <button type="button" onClick={onClose} className="cancel-button">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}

EditProjectModal.propTypes = {
  project: PropTypes.shape({
    id: PropTypes.string.isRequired,
    title: PropTypes.string,
    description: PropTypes.string,
    imageUrl: PropTypes.string,
  }),
  onClose: PropTypes.func.isRequired,
  refreshProjects: PropTypes.func.isRequired,
};

export default EditProjectModal;
