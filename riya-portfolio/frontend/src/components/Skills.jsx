const skillGroups = [
  {
    title: 'Programming',
    items: ['Python', 'SQL', 'HTML', 'CSS', 'Data Structures & Algorithms'],
  },
  {
    title: 'Machine Learning',
    items: ['Regression', 'Classification', 'Clustering', 'Feature Engineering', 'Model Evaluation', 'Data Analysis'],
  },
  {
    title: 'Backend',
    items: ['Django', 'Django REST Framework', 'REST APIs', 'Serializers', 'ViewSets'],
  },
  {
    title: 'Libraries',
    items: ['NumPy', 'Pandas', 'Matplotlib', 'Seaborn', 'Scikit-learn', 'TensorFlow', 'Flask'],
  },
  {
    title: 'Databases',
    items: ['PostgreSQL / MySQL'],
  },
  {
    title: 'Tools',
    items: ['Git', 'Linux', 'Docker', 'Jupyter Notebook', 'VS Code'],
  },
  {
    title: 'Cloud',
    items: ['AWS EC2', 'AWS S3', 'AWS IAM'],
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
