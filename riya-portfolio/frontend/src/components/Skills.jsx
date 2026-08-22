const skillGroups = [
  {
    title: 'Programming',
    items: ['Python', 'JavaScript', 'SQL', 'HTML', 'CSS', 'Data Structures & Algorithms'],
  },
  {
    title: 'Machine Learning & AI',
    items: ['LangChain', 'LangGraph', 'RAG', 'FAISS', 'Hugging Face Inference API', 'Prompt Engineering', 'Regression', 'Classification', 'Clustering', 'Feature Engineering', 'Model Evaluation'],
  },
  {
    title: 'Computer Vision',
    items: ['OpenCV', 'Edge Detection', 'Face Detection', 'TensorFlow', 'Image Classification'],
  },
  {
    title: 'Backend',
    items: ['Django', 'Django REST Framework', 'FastAPI', 'REST APIs', 'Serializers', 'ViewSets'],
  },
  {
    title: 'MERN Stack',
    items: ['Node.js', 'Express', 'MongoDB', 'Mongoose', 'React'],
  },
  {
    title: 'Databases',
    items: ['PostgreSQL', 'MySQL', 'MongoDB'],
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
