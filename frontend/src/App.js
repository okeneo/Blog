import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/home/Home";
import About from "./pages/about/About"
import Blog from "./pages/blog/Blog"
import Projects from "./pages/projects/Projects"
import Art from "./pages/art/Art";
import Register from "./pages/register/Register"
import Login from "./pages/login/Login"
import Navbar from "./components/Navbar";

function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/about" element={<About />} />
          <Route exact path="/blog" element={<Blog />} />
          <Route exact path="/projects" element={<Projects />} />
          <Route exact path="/art" element={<Art />} />
          <Route exact path="/register" element={<Register />} />
          <Route exact path="/login" element={<Login />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;