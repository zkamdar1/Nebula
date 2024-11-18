import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import './ProjectPage.css';

function ProjectPage() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [activeTab, setActiveTab] = useState('background'); // Tab state for the left card


  useEffect(() => {
    const fetchProject = async () => {
      try {
        const response = await api.get(`/projects/${projectId}`);
        setProject(response.data);
      } catch (error) {
        console.error('Error fetching project:', error);
      }
    };

    fetchProject();
  }, [projectId]);

  if (!project) return <p>Loading...</p>;

  const renderAssets = () => {
    const assets = activeTab === 'background' ? ['clip1.mp4', 'clip2.mp4'] : ['music1.mp3', 'music2.mp3'];
    return assets.map((asset, index) => (
      <div key={index} className="asset-item">
        {activeTab === 'background' ? (
          <video src={`/backend/video_generator/background_clips/${asset}`} controls className="asset-preview" />
        ) : (
          <audio src={`/backend/video_generator/music_clips/${asset}`} controls className="asset-preview" />
        )}
      </div>
    ));
  };

  const renderFinalVideos = () => {
    const finalVideos = ['output1.mp4', 'output2.mp4'];
    return finalVideos.map((video, index) => (
      <div key={index} className="asset-item">
        <video src={`/backend/video_generator/final_videos/${video}`} controls className="asset-preview" />
      </div>
    ));
  };

  return (
   <div className="project-page">
      {/* Top Half */}
      <div className="top-half">
        {/* Left Card: Assets */}
        <div className="assets-card">
          <div className="tabs">
            <button className={activeTab === 'background' ? 'active' : ''} onClick={() => setActiveTab('background')}>
              Background Clips
            </button>
            <button className={activeTab === 'music' ? 'active' : ''} onClick={() => setActiveTab('music')}>
              Music Clips
            </button>
          </div>
          <div className="assets-container">{renderAssets()}</div>
        </div>

        {/* Middle Card: Video Preview */}
        <div className="preview-card">
          <video controls className="video-preview">
            <source src={project.currentVideoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>

        {/* Right Card: Final Videos */}
        <div className="final-videos-card">
          <h3>Final Videos</h3>
          <div className="assets-container">{renderFinalVideos()}</div>
        </div>
      </div>

      {/* Bottom Half */}
      <div className="bottom-half">
        <h2>Customize and Generate</h2>
        <div className="filters-container">
          <label>Font:</label>
          <select>
            <option>Default</option>
            <option>Modern</option>
            <option>Classic</option>
          </select>

          <label>Subtitle Style:</label>
          <select>
            <option>Minimal</option>
            <option>Dynamic</option>
          </select>
        </div>
        <button className="generate-button">Generate Video</button>
      </div>
    </div>
  );
}

export default ProjectPage;
