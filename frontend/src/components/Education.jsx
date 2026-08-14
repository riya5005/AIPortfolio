function Education() {
  return (
    <section className="education" id="education">
      <h2 className="section-title">Education</h2>

      <div className="education-card">
        <div className="education-header">
          <div>
            <h3>B.Tech in Computer Science (Data Science)</h3>
            <p className="college">
              ABES Institute of Technology
            </p>
            <p className="university">
              Dr. A.P.J. Abdul Kalam Technical University (AKTU)
            </p>
          </div>

          <span className="education-year">
            2023 – 2027
          </span>
        </div>

        <div className="education-divider"></div>

        <h4>Focus Areas</h4>

        <div className="focus-tags">
          <span>Machine Learning</span>
          <span>Artificial Intelligence</span>
          <span>Python</span>
          <span>Django</span>
          <span>PostgreSQL</span>
          <span>Data Structures</span>
          <span>Cloud Computing</span>
        </div>
      </div>
    </section>
  );
}

export default Education;