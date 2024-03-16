import React from "react";
import './Home.css';

function HomePage() {
    return (
        <div className="home-container">
            <div className="development-message">
                <p><span className="red-text"> This frontened is currently under construction.</span> View the <a href="https://github.com/okeneo/PersonalNest" target="_blank">repository</a> and API <a href="https://okeneo.github.io/PersonalNest/" target="_blank">documentation</a>.</p>
            </div>
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
            <div className="current-work">
                <h3>Currently focusing on:</h3>
                <ul>
                    <li>Studying for exams.</li>
                    <li>Developing <a href="https://github.com/UMUAS/Nav2023-2024" target="_blank">software</a> for a semi-autonomous drone for the National Student RPAS Competition in Montreal.</li>
                </ul>
            </div>
            {/* <div className="recent-blog-posts">
                <h3>Recent Blog Posts</h3>
            </div> */}
        </div>
    );
}

export default HomePage;
