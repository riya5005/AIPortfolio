function About() {
  return (
    <section id="about">
      <h2 className="section-title">About</h2>
      <div className="about-card">
        <p>
          I'm a B.Tech Computer Science student focused on building AI systems that
          actually work in production — not just in a notebook. My core work is in
          Agentic AI and Retrieval-Augmented Generation, using LangChain, LangGraph,
          and FAISS to build LLM-powered applications with real guardrails around them.
        </p>
        <p>
          This site itself is a live example: a RAG chatbot with input/output security
          checks, a Computer Vision demo (OpenCV + a deep learning classifier), and a
          MERN-stack guestbook (Node.js, Express, MongoDB) — each piece deployed as its
          own service, using whichever stack actually fits the problem best.
        </p>
      </div>
    </section>
  )
}

export default About
