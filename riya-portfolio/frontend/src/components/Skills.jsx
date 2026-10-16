const skillGroups = [
  {
    title: 'Programming',
    items: ['Python', 'JavaScript', 'SQL', 'HTML', 'CSS', 'Data Structures & Algorithms', 'OOP'],
  },
  {
    title: 'AI & LLMs',
    items: ['LangChain', 'LangGraph', 'RAG', 'FAISS', 'LLM-based Applications', 'Prompt Engineering'],
  },
  {
    title: 'Machine Learning & Computer Vision',
    items: ['Scikit-learn', 'TensorFlow', 'Regression', 'Classification', 'Model Evaluation'],
  },
  {
    title: 'MERN Stack',
    items: ['MongoDB', 'Express', 'React', 'Node.js', 'Mongoose'],
  },
  {
    title: 'Backend & APIs',
    items: ['FastAPI', 'REST APIs'],
  },
  {
    title: 'Databases',
    items: ['MongoDB', 'PostgreSQL', 'MySQL'],
  },
]

function Skills() {
  return (
    <section id="skills">
      <h2 className="section-title">Technical Skills</h2>
      <div className="skills-grid">
        {skillGroups.map((group) => (
          <div className="skill-card" key={group.title}>
            <h4>{group.title}</h4>
            <div className="skill-tags">
              {group.items.map((item) => (
                <span key={item}>{item}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

export default Skills
