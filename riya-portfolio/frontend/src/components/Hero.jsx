function Hero() {
  return (
    <section className="hero">
      <div className="hero-row">
        <img
          className="hero-photo"
          src="/riya-photo.jpg"
          alt="Riya Sharma"
          onError={(e) => {
            e.target.onerror = null
            e.target.src = 'https://ui-avatars.com/api/?name=Riya+Sharma&background=dfe6d4&color=1f1d1a&size=220'
          }}
        />
        <div className="hero-text">
         <h1>Riya Sharma</h1>

<p className="role">
  Machine Learning &amp; Backend Developer
</p>

<p className="hero-tagline">
  Turning ideas into intelligent solutions with Machine Learning and AI.
  Currently exploring LLMs, RAG and building projects that solve real-world problems.
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