function Hero() {
  return (
    <section className="hero">
      <div className="hero-row">
        <img
          className="hero-photo"
          src="/riya-photo.jpg"
          alt="Riya"
          onError={(e) => {
            e.target.onerror = null
            e.target.src = 'https://ui-avatars.com/api/?name=Riya+Sharma&background=dfe6d4&color=1f1d1a&size=220'
          }}
        />
        <div className="hero-text">
         <h1>Riya Kumari</h1>

<p className="role">Software Developer | CS Fundamentals &amp; Backend</p>

<p className="hero-tagline">
  CS undergrad building real, deployed software — strong in DSA and core
  fundamentals, currently learning Java, with hands-on experience in
  AI systems and full-stack development.
</p>
          <div className="hero-links">
            <a href="https://github.com/riya5005" target="_blank" rel="noreferrer">GitHub ↗</a>
            <a href="https://linkedin.com/in/riya-sharma" target="_blank" rel="noreferrer">LinkedIn ↗</a>
            <a href="mailto:riya.sharma@example.com">Email</a>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero
