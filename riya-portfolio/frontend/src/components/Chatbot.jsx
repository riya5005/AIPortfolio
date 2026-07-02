import { useState, useRef, useEffect } from 'react'

// Change this if your backend runs somewhere else
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const suggestedPrompts = [
  'What are Riya\'s qualifications?',
  'Which tech stack does Riya know?',
  'Tell me about her ML projects',
  'Give me her LinkedIn and GitHub links',
]

function Chatbot() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'bot', text: "Hi! I'm Riya's portfolio assistant. Ask me about her skills, projects, or education — or tap a suggestion below." },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bodyRef = useRef(null)

  useEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight
    }
  }, [messages, loading])

  async function sendMessage(text) {
    if (!text.trim()) return
    setMessages((prev) => [...prev, { role: 'user', text }])
    setInput('')
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      })
      if (!res.ok) throw new Error('Request failed')
      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'bot', text: data.answer }])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'bot', text: "I couldn't reach the backend. Make sure the FastAPI server is running on " + API_URL },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <button className="chat-toggle" onClick={() => setOpen((o) => !o)} aria-label="Toggle chatbot">
        {open ? '✕' : '💬'}
      </button>

      {open && (
        <div className="chat-window">
          <div className="chat-header">
            Ask about Riya
            <span>RAG chatbot · LangChain + LangGraph</span>
          </div>

          <div className="chat-body" ref={bodyRef}>
            {messages.map((m, i) => (
              <div className={`chat-msg ${m.role}`} key={i}>{m.text}</div>
            ))}
            {loading && <div className="chat-loading">thinking…</div>}
          </div>

          <div className="chat-suggestions">
            {suggestedPrompts.map((p) => (
              <button key={p} onClick={() => sendMessage(p)}>{p}</button>
            ))}
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={input}
              placeholder="Type a question..."
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage(input)}
            />
            <button onClick={() => sendMessage(input)}>Send</button>
          </div>
        </div>
      )}
    </>
  )
}

export default Chatbot
