import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Container } from "react-bootstrap";

class Home extends Component {
    render() {
        return (
            <Container>
                <h1>Home</h1>
                <p>
                    <Link to="/register/">Register</Link>
                </p>
                <p>
                    <Link to="/login/">Login</Link>
                </p>
                <p>
                    <Link to="/about/">About</Link>
                </p>
                <p>
                    <Link to="/blog/">Blog</Link>
                </p>
            </Container>
        );
    }
}

export default Home;