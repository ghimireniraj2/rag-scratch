import { useState } from "react"

export default function App() {
  const [input, setInput] = useState("")
  const [messages, setMessages] = useState([])

  async function handleSubmit() {
    if (!input.trim()) return
    const question = input
    setMessages(prev => [...prev, { question, answer: "", sources: [] }])
    setInput("")

    const response = await fetch("http://localhost:8000/ask-stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, k: 5 })
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ""

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split("\n")
      buffer = lines.pop()

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue
        const data = JSON.parse(line.replace("data: ", ""))
        if (data.done) {
          setMessages(prev => {
            const updated = [...prev]
            updated[updated.length - 1].sources = data.sources
            return updated
          })
        } else if (data.delta) {
          setMessages(prev => {
            const updated = [...prev]
            updated[updated.length - 1].answer += data.delta
            return updated
          })
        }
      }
    }
  }

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "20px" }}>
      <div style={{ marginBottom: "20px" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: "24px" }}>
            <p><strong>Q:</strong> {m.question}</p>
            <p><strong>A:</strong> {m.answer}</p>
            {m.sources.length > 0 && <SourceAccordion sources={m.sources} />}
          </div>
        ))}
      </div>
      <div style={{ display: "flex", gap: "8px", alignItems: "flex-end" }}>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask a question..."
          rows={4}
          style={{ flex: 1, padding: "8px 12px", fontSize: "14px", border: "1px solid #ccc", borderRadius: "4px", resize: "vertical", width: "800px" }}
        />
        <button
          onClick={handleSubmit}
          style={{ padding: "8px 16px", fontSize: "14px", color: "#fff", background: "#0d6efd", border: "none", borderRadius: "4px", cursor: "pointer", whiteSpace: "nowrap" }}
        >
          Ask
        </button>
      </div>
    </div>
  )
}

function SourceAccordion({ sources }) {
  const [open, setOpen] = useState(false)
  return (
    <div style={{ marginTop: "8px", border: "1px solid #ddd", borderRadius: "4px" }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{ width: "100%", textAlign: "left", padding: "8px 12px", background: "#f8f9fa", border: "none", cursor: "pointer", fontSize: "13px" }}
      >
        {open ? "▾" : "▸"} Sources ({sources.length})
      </button>
      {open && (
        <div style={{ padding: "8px 12px" }}>
          {sources.map((s, i) => (
            <div key={i} style={{ marginBottom: "12px", fontSize: "12px", borderBottom: "1px solid #eee", paddingBottom: "8px" }}>
              <div style={{ color: "#666" }}><strong>{s.source}</strong> — page {s.page} — score {s.score.toFixed(2)}</div>
              <div style={{ marginTop: "4px", color: "#444" }}>{s.text.slice(0, 200)}...</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}