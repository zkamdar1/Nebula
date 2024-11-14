// src/components/ProjectCard.js
import React from 'react';
import './ProjectCard.css';
import { FaPencilAlt } from 'react-icons/fa';

function ProjectCard({ title, description, lastAccessed, imageUrl, onEdit }) {

    const formattedDate = new Date(lastAccessed).toLocaleString();

    const handleEditClick = (e) => {
        e.stopPropagation(); // Prevent triggering card's onClick if any
        onEdit(); // Pass necessary project data
    };

    return (
        <div className="project-card">
            <FaPencilAlt className="edit-icon" onClick={handleEditClick} title="Edit Project" />
             <div
                className={`project-image ${imageUrl ? 'with-image' : 'no-image'}`}
                style={imageUrl ? { backgroundImage: `url(${imageUrl})` } : {}}
            />
            <div className="project-info">
                <h3 className="project-title">{title}</h3>
                <p className="project-description">{description}</p>
                <p className="project-last-accessed">Last accessed: {formattedDate}</p>
            </div>
        </div>
    );
}

export default ProjectCard;
