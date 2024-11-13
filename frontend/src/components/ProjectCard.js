// src/components/ProjectCard.js
import React from 'react';
import './ProjectCard.css';

function ProjectCard({ title, description, lastAccessed, imageUrl }) {
    return (
        <div className="project-card">
             <div
                className={`project-image ${imageUrl ? 'with-image' : 'no-image'}`}
                style={imageUrl ? { backgroundImage: `url(${imageUrl})` } : {}}
            />
            <div className="project-info">
                <h3 className="project-title">{title}</h3>
                <p className="project-description">{description}</p>
                <p className="project-last-accessed">Last accessed: {lastAccessed}</p>
            </div>
        </div>
    );
}

export default ProjectCard;
