"""
This is Riya's 'knowledge base' — the source of truth the chatbot retrieves
from. Edit this file whenever your resume changes; the vector index will
rebuild automatically the next time the server starts (see vectorstore.py).
"""

from langchain.docstore.document import Document

RAW_FACTS = [
    {
        "topic": "about",
        "text": (
            "Riya Sharma is a B.Tech Computer Science & Engineering (Data Science) "
            "student at ABES Institute of Technology, AKTU. She specializes in "
            "Machine Learning and backend development, building end-to-end ML "
            "pipelines and shipping them as real REST APIs using Python and Django."
        ),
    },
    {
        "topic": "links",
        "text": (
            "Riya's GitHub profile is https://github.com/riya5005. "
            "Her LinkedIn profile is https://linkedin.com/in/riya-sharma. "
            "You can reach her by email as well through the portfolio site."
        ),
    },
    {
        "topic": "education",
        "text": (
            "Riya is pursuing a Bachelor of Technology (B.Tech) in Computer Science "
            "& Engineering with a specialization in Data Science at ABES Institute "
            "of Technology, affiliated with AKTU (Dr. A.P.J. Abdul Kalam Technical "
            "University)."
        ),
    },
    {
        "topic": "skills-programming",
        "text": (
            "Riya's programming skills include Python, SQL, HTML, CSS, and a solid "
            "foundation in Data Structures & Algorithms."
        ),
    },
    {
        "topic": "skills-ml",
        "text": (
            "In Machine Learning, Riya has hands-on experience with Regression, "
            "Classification, Clustering, Feature Engineering, Model Evaluation "
            "(ROC-AUC, Precision, Recall, F1-score), and Data Analysis."
        ),
    },
    {
        "topic": "skills-backend",
        "text": (
            "On the backend, Riya works with Django, Django REST Framework (DRF), "
            "building REST APIs, serializers, and ViewSets to expose ML models as "
            "production-ready endpoints."
        ),
    },
    {
        "topic": "skills-libraries",
        "text": (
            "Riya's core ML/data libraries are NumPy, Pandas, Matplotlib, Seaborn, "
            "Scikit-learn, TensorFlow, and Flask."
        ),
    },
    {
        "topic": "skills-tools-cloud",
        "text": (
            "Her tools include Git, Linux, Docker, Jupyter Notebook, and VS Code. "
            "For databases she uses MySQL, and for cloud she knows AWS fundamentals: "
            "EC2, S3, and IAM."
        ),
    },
    {
        "topic": "project-fraud-detection",
        "text": (
            "Project: Credit Card Fraud Detection System. Riya built an end-to-end "
            "ML pipeline in Python and Scikit-learn to detect fraudulent transactions. "
            "She handled the imbalanced dataset using SMOTE to improve minority-class "
            "detection, trained Logistic Regression and Random Forest models, and "
            "evaluated them with ROC-AUC, Precision, Recall, and F1-score, reaching a "
            "ROC-AUC score of 0.94. She migrated the backend from Flask to Django REST "
            "Framework, exposing the prediction as a REST API with serializer-based "
            "input validation. GitHub: github.com/riya5005/credit-card-fraud-detection_Django. "
            "Live demo: credit-card-fraud-detection-django.onrender.com."
        ),
    },
    {
        "topic": "project-house-price",
        "text": (
            "Project: House Price Prediction Web Application. Riya built a regression "
            "model on the California Housing dataset (20,640 records, 8 features), "
            "achieving an R² of about 0.82 using Random Forest. She built a complete "
            "ML pipeline (preprocessing, feature scaling, training, prediction) and a "
            "Django-based web application with a REST API for real-time predictions, "
            "optimized for fast and reliable responses. GitHub: "
            "github.com/riya5005/housing-price-prediction-fullstack. Live demo: "
            "california-housing-predictions-django.onrender.com."
        ),
    },
    {
        "topic": "qualifications-summary",
        "text": (
            "Summary of Riya's qualifications: B.Tech in CSE (Data Science) from "
            "ABES Institute of Technology (AKTU); practical experience across the "
            "full ML lifecycle from data preprocessing to model deployment; two "
            "deployed ML-powered web applications with REST APIs; strong grip on "
            "Python, Django REST Framework, and Scikit-learn."
        ),
    },
]


def load_documents() -> list[Document]:
    """Convert the raw facts into LangChain Documents for embedding."""
    return [
        Document(page_content=item["text"], metadata={"topic": item["topic"]})
        for item in RAW_FACTS
    ]
