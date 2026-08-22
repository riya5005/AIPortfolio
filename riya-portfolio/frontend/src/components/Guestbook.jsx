import { useState, useEffect } from 'react'

const GUESTBOOK_API_URL = 'https://aiportfolio-1-83ch.onrender.com'

function Guestbook() {
  const [messages, setMessages] = useState([])
  const [name, setName] = useState('')
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [showMessages, setShowMessages] = useState(false)
  const [fetched, setFetched] = useState(false)

  function loadMessages() {
    fetch(`${GUESTBOOK_API_URL}/api/messages`)
      .then((res) => res.json())
      .then((data) => {
        setMessages(data)
        setFetched(true)
      })
  }

  function toggleMessages() {
    if (!showMessages && !fetched) {
      loadMessages()
    }
    setShowMessages((prev) => !prev)
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (!name.trim() || !text.trim()) return

    setLoading(true)
    fetch(`${GUESTBOOK_API_URL}/api/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, text }),
    })
      .then((res) => res.json())
      .then((newMsg) => {
        setMessages((prev) => [newMsg, ...prev])
        setFetched(true)
        setName('')
        setText('')
      })
      .finally(() => setLoading(false))
  }

  return (
    <section id="guestbook">
      <h2 className="section-title">Guestbook</h2>
      <div className="guestbook-card">
        <p>Leave a note — built with Node.js, Express, and MongoDB.</p>

        <form onSubmit={handleSubmit} className="guestbook-form">
          <input
            placeholder="Your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            maxLength={60}
          />
          <input
            placeholder="Say something"
            value={text}
            onChange={(e) => setText(e.target.value)}
            maxLength={300}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Posting...' : 'Post'}
          </button>
        </form>

        <button className="guestbook-toggle" onClick={toggleMessages}>
          {showMessages ? 'Hide messages' : 'View messages'}
        </button>

        {showMessages && (
          <div className="guestbook-list">
            {fetched && messages.length === 0 && (
              <p className="guestbook-empty">No messages yet — be the first to say hi!</p>
            )}
            {messages.map((m) => (
              <div className="guestbook-entry" key={m._id}>
                <span className="guestbook-name">{m.name}</span>
                <span className="guestbook-text">{m.text}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

export default Guestbook
