import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import About from './components/About.jsx'
import Skills from './components/Skills.jsx'
import Projects from './components/Projects.jsx'
import Education from './components/Education.jsx'
import Footer from './components/Footer.jsx'
import Chatbot from './components/Chatbot.jsx'

function App() {
  return (
    <div>
      <Navbar />
      <div className="container">
        <Hero />
        <About />
        <Skills />
        <Projects />
        <Education />
      </div>
      <Footer />
      <Chatbot />
    </div>
  )
}

export default App