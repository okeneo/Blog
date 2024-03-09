import React from "react";
import './Home.css';

function HomePage() {
    return (
        <div className="home-container">
            <div className="profile-container">
                <img
                    className="profile-picture"
                    src={require("./personal-portrait.jpg")}
                    alt="Tega Okene"
                />
                <div className="info-container">
                    <h1>Tega Okene</h1>
                    <h2>Computer Science and Mathematics Student</h2>
                </div>
            </div>
            <div className="recent-blog-posts">
                <h3>Recent Blog Posts</h3>
            </div>
        </div>
    );
}

export default HomePage;
