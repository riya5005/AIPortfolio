import { useState, useEffect } from 'react'

function Guestbook() {
  const [messages, setMessages] = useState([])
  const [name, setName] = useState('')
  const [text, setText] = useState('')

  // Load messages when the page opens
  useEffect(() => {
    fetch('https://aiportfolio-1-83ch.onrender.com/api/messages')
      .then((res) => res.json())
      .then((data) => setMessages(data))
  }, [])

  // Send a new message
  function handleSubmit(e) {
    e.preventDefault()
    fetch('https://aiportfolio-1-83ch.onrender.com/api/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, text }),
    })
      .then((res) => res.json())
      .then((newMsg) => {
        setMessages([newMsg, ...messages])
        setName('')
        setText('')
      })
  }

  return (
    <section id="guestbook">
      <h2 className="section-title">Guestbook</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          placeholder="Say something"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button type="submit">Post</button>
      </form>

      {messages.map((m) => (
        <p key={m._id}><strong>{m.name}:</strong> {m.text}</p>
      ))}
    </section>
  )
}

export default Guestbook
