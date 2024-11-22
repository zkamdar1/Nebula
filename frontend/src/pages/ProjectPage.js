import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import './ProjectPage.css';

function ProjectPage() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [activeTab, setActiveTab] = useState('background'); // Tab state for the left card
  const [assets, setAssets] = useState([]);
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

  const fetchMedia = async () => {
      const mediaType = activeTab === "background" ? "background_clips" : "music_clips";

    try {
      const response = await api.get(`/media/${projectId}/${mediaType}`);
      setAssets(response.data); // Store all media in one state
    } catch (error) {
      console.error("Error fetching media:", error);
    }
  };

  useEffect(() => {
    fetchMedia();
  }, [projectId, activeTab]);

  const filteredAssets = assets.filter((asset) =>
  activeTab === "background"
    ? asset.media_type === "background_clips"
    : asset.media_type === "music_clips"
  );

  const handleFileUpload = async (event) => {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const mediaType = document.getElementById("media-type").value;

    if (!file) return;

    const formData = new FormData();
    formData.append("project_id", projectId);
    formData.append("media_type", mediaType);
    formData.append("file", file);

    try {
      await api.post("/media/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("File uploaded successfully!");
      fetchMedia(); // Refresh media
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file.");
    } finally {
      fileInput.value = "";
    }
  };



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
            {filteredAssets.map((asset) => (
              <div key={asset.id} className="asset-item" onClick={() => setSelectedMedia(asset.media_url)}>
              {asset.media_url.endsWith('.mp4') ? (
                <video className="thumbnail" width="100%" height="auto" controls>
                  <source src={asset.media_url} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              ) : asset.media_url.endsWith('.mp3') ? (
                <audio className="thumbnail" controls>
                  <source src={asset.media_url} type="audio/mp3" />
                  Your browser does not support the audio tag.
                </audio>
              ) : (
                <img src="/placeholder-thumbnail.png" alt="Thumbnail" className="thumbnail" />
              )}
            </div>
            ))}
          </div>
        </div>

        {/* Middle Card: Video Preview */}
        <div className="preview-card">
          {selectedMedia ? (
            selectedMedia.endsWith('.mp4') ? (
              <video controls className="video-preview">
                <source src={selectedMedia} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            ) : (
              <audio controls className="audio-preview">
                <source src={selectedMedia} type="audio/mp3" />
                Your browser does not support the audio tag.
              </audio>
            )
          ) : (
            <p>Select media to preview</p>
          )}
        </div>

        {/* Right Card: Final Videos */}
        <div className="final-videos-card">
          <h3>Final Videos</h3>
          <div className="assets-container">
            {filteredAssets.map((video) => (
              <div key={video.id} className="asset-item" onClick={() => setSelectedMedia(video.media_url)}>
                <img src={selectedMedia} alt="Thumbnail" className="thumbnail" />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Half */}
      <div className="bottom-half">
        <div className="bottom-header">
          <h2>Customize and Generate</h2>
          <div className="upload-container">
            <select id="media-type" defaultValue="background_clips">
              <option value="background_clips">Background Clips</option>
              <option value="music_clips">Music Clips</option>
            </select>
            <input
              type="file"
              id="file-upload"
              onChange={handleFileUpload}
              style={{ display: "none" }}
            />
            <label htmlFor="file-upload" className="upload-button">
              Upload Media
            </label>
          </div>
        </div>
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
