function About() {
  return (
    <section id="about">
      <h2 className="section-title">About</h2>
      <div className="about-card">
        <p>
          I'm a B.Tech Computer Science &amp; Engineering (Data Science) student at
          ABES Institute of Technology, AKTU, with a soft spot for turning messy,
          real-world data into models that actually hold up in production — not just
          in a notebook.
        </p>
        <p>
          Most of my work sits at the intersection of Machine Learning and backend
          engineering: I train and evaluate models with Scikit-learn and TensorFlow,
          then wrap them in Django REST Framework so they're usable as real APIs, not
          just static predictions. My fraud detection and housing price projects (below)
          both follow this same end-to-end approach — from raw data to a deployed,
          testable service.
        </p>
        <p>
          Right now I'm going deeper into LLMs, Retrieval-Augmented Generation, and
          agentic AI — the chatbot on this very site is one of those experiments,
          built with LangChain, LangGraph, FAISS, and an open-source model served
          through Hugging Face.
        </p>
      </div>
    </section>
  )
}

export default About
