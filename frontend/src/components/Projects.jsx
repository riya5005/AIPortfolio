const projects = [
  {
    title: 'Credit Card Fraud Detection System',
    points: [
      'Built an end-to-end ML pipeline using Python and Scikit-learn for fraud detection',
      'Handled imbalanced dataset using SMOTE, improving minority class detection',
      'Trained Logistic Regression and Random Forest models, evaluated using ROC-AUC, Precision, Recall, and F1-score',
      'Achieved ROC-AUC score of 0.94',
      'Migrated backend from Flask to Django REST Framework, exposing predictions as a REST API with serializer-based validation',
    ],
    github: 'https://github.com/riya5005/credit-card-fraud-detection_Django',
    demo: 'https://credit-card-fraud-detection-django.onrender.com',
  },
  {
    title: 'House Price Prediction Web Application',
    points: [
      'Built a regression model on the California Housing dataset (20,640 records, 8 features), achieving R² ≈ 0.82 with Random Forest',
      'Developed a complete end-to-end ML pipeline: preprocessing, feature scaling, training, prediction',
      'Designed a Django-based web application with a REST API for real-time predictions',
      'Optimized the backend for fast, reliable predictions',
    ],
    github: 'https://github.com/riya5005/housing-price-prediction-fullstack',
    demo: 'https://california-housing-predictions-django.onrender.com',
  },
]

function Projects() {
  return (
    <section id="projects">
      <h2 className="section-title">Projects</h2>
      {projects.map((p) => (
        <div className="project-card" key={p.title}>
          <h3>{p.title}</h3>
          <ul>
            {p.points.map((pt, i) => (
              <li key={i}>{pt}</li>
            ))}
          </ul>
          <div className="project-links">
            <a href={p.github} target="_blank" rel="noreferrer">GitHub →</a>
            <a href={p.demo} target="_blank" rel="noreferrer">Live Demo →</a>
          </div>
        </div>
      ))}
    </section>
  )
}

export default Projects
