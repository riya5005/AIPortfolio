import express from 'express'
import mongoose from 'mongoose'
import cors from 'cors'
import dotenv from 'dotenv'

dotenv.config()

// Connect to the database
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch((err) => console.log('MongoDB error:', err))

// Describe what a "message" looks like in the database
const Message = mongoose.model('Message', {
  name: String,
  text: String,
  createdAt: { type: Date, default: Date.now },
})

const app = express()
app.use(express.json())
app.use(cors())

// Simple health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' })
})

// Show all messages
app.get('/api/messages', async (req, res) => {
  const messages = await Message.find().sort({ createdAt: -1 })
  res.json(messages)
})

// Save a new message
app.post('/api/messages', async (req, res) => {
  const newMessage = await Message.create({
    name: req.body.name,
    text: req.body.text,
  })
  res.json(newMessage)
})

const PORT = process.env.PORT || 4000
app.listen(PORT, () => console.log(`Guestbook server running on port ${PORT}`))
