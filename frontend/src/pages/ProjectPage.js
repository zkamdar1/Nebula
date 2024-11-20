import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import './ProjectPage.css';

function ProjectPage() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [activeTab, setActiveTab] = useState('background'); // Tab state for the left card
  const [assets, setAssets] = useState([]);
  const [finalVideos, setFinalVideos] = useState([]);
  const [selectedMedia, setSelectedMedia] = useState(null);


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

  const fetchAssets = async (type) => {
    try {
      const response = await api.get(`/media/${type}`);
      setAssets(response.data.files);
    } catch (error) {
      console.error(`Error fetching ${type}:`, error);
    }
  };

  useEffect(() => {
    fetchAssets(activeTab === 'background' ? 'background_clips' : 'music_clips');
  }, [activeTab]);

  const handleGenerateVideo = async () => {
    try {
      await api.post(`/projects/${projectId}/generate`);
      alert('Video generation started!');
    } catch (error) {
      console.error('Error generating video:', error);
      alert('Failed to generate video.');
    }
  };

  if (!project) return <p>Loading...</p>;

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
          <div className="assets-container">
            {assets.map((asset, index) => (
              <div
                key={index}
                className="asset-item"
                onClick={() => setSelectedMedia(asset)}
              >
              </div>
            ))}
          </div>
        </div>

        {/* Middle Card: Video Preview */}
        <div className="preview-card">
          {selectedMedia ? (
            selectedMedia.endsWith('.mp4') ? (
              <video controls className="video-preview">
                <source src={`/media/${selectedMedia}`} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            ) : (
              <audio controls className="audio-preview">
                <source src={`/media/${selectedMedia}`} type="audio/mp3" />
                Your browser does not support the audio tag.
              </audio>
            )
          ) : (
            <video controls className="video-preview">
              <source src={`/media/${finalVideos[0]}`} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          )}
        </div>

        {/* Right Card: Final Videos */}
        <div className="final-videos-card">
          <h3>Final Videos</h3>
          <div className="assets-container">
            {finalVideos.map((video, index) => (
              <div
                key={index}
                className="asset-item"
                onClick={() => setSelectedMedia(video)}
              >
              </div>
            ))}
          </div>
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
        <button className="generate-button" onClick={handleGenerateVideo}>Generate Video</button>
      </div>
    </div>
  );
}

export default ProjectPage;
