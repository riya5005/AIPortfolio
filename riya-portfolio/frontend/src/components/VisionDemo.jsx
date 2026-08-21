import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function VisionDemo() {
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleFile(e) {
    const file = e.target.files[0]
    if (!file) return

    setPreview(URL.createObjectURL(file))
    setResult(null)
    setError(null)
    setLoading(true)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(`${API_URL}/api/vision/analyze`, {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (data.error) {
        setError(data.error)
      } else {
        setResult(data)
      }
    } catch (err) {
      setError("Couldn't reach the backend for image analysis.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <section id="vision">
      <h2 className="section-title">Computer Vision Demo</h2>
      <div className="vision-card">
        <p>
          Upload a photo to see live OpenCV analysis (edge detection, face
          detection) and deep learning image classification (MobileNetV2) —
          processed entirely on the backend.
        </p>
        <input type="file" accept="image/*" onChange={handleFile} />

        {loading && <p className="chat-loading">Analyzing image…</p>}
        {error && <p className="vision-error">{error}</p>}

        {result && (
          <div className="vision-results">
            <div className="vision-images">
              <div>
                <p className="vision-label">Faces detected: {result.faces_detected}</p>
                <img
                  src={`data:image/jpeg;base64,${result.annotated_image_base64}`}
                  alt="Face detection result"
                  className="vision-img"
                />
              </div>
              <div>
                <p className="vision-label">Edge detection</p>
                <img
                  src={`data:image/jpeg;base64,${result.edges_image_base64}`}
                  alt="Edge detection result"
                  className="vision-img"
                />
              </div>
            </div>

            {result.predictions && result.predictions.length > 0 && (
              <div className="vision-predictions">
                <p className="vision-label">Deep learning classification (MobileNetV2)</p>
                <ul>
                  {result.predictions.map((p, i) => (
                    <li key={i}>{p.label} — {(p.confidence * 100).toFixed(1)}%</li>
                  ))}
                </ul>
              </div>
            )}

            <p className="vision-stats">
              {result.width}×{result.height}px · edge pixel ratio: {result.edge_pixel_ratio}
            </p>
          </div>
        )}
      </div>
    </section>
  )
}

export default VisionDemo
