import React, { Component, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Container, Button, Row, Col, Form, FormControl } from "react-bootstrap";

// class Register extends Component {
//     render() {
//         return (
//             <Container>
//                 <h1>Register</h1>
//             </Container>
//         );
//     }
// }

function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password1, setPassword1] = useState("");
    const [password2, setPassword2] = useState("");

    const navigate = useNavigate();
}

export default Register;