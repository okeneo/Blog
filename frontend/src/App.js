import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./components/Home";
import Register from "./components/register/Register"
import Login from "./components/login/Login"
import Blog from "./components/blog/Blog"
import About from "./components/about/About"

function App() {
    return (
      <div className="App">
        <Router>
          <Routes>
            <Route exact path="/" element={<Home/>} />
            <Route exact path="/register" element={<Register/>} />
            <Route exact path="/login" element={<Login/>} />
            <Route exact path="/blog" element={<Blog/>} />
            <Route exact path="/about" element={<About/>} />
          </Routes>
        </Router>
      </div>
    );
}

export default App;