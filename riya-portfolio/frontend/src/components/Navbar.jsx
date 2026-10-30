import { useState } from 'react'

function Navbar() {
  const [theme, setTheme] = useState(
    document.documentElement.getAttribute('data-theme') || 'light'
  )

  function toggleTheme() {
    const next = theme === 'dark' ? 'light' : 'dark'
    setTheme(next)
    document.documentElement.setAttribute('data-theme', next)
    try { localStorage.setItem('theme', next) } catch (e) {}
  }

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <div className="logo">riya.dev</div>
        <ul>
          <li><a href="#about">About</a></li>
          <li><a href="#skills">Skills</a></li>
          <li><a href="#projects">Projects</a></li>
          <li><a href="#vision">Vision Demo</a></li>
          <li><a href="#education">Education</a></li>
          <li><a href="#guestbook">Guestbook</a></li>
        </ul>
        <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle dark mode">
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
      </div>
    </nav>
  )
}

export default Navbar
