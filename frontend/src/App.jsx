import { useEffect, useState } from 'react'
import './App.css'

const API = '/api/books'
const STATUSES = ['to-read', 'reading', 'done']
const EMPTY = { title: '', author: '', status: 'to-read', rating: '' }
const JSON_HEADERS = { 'Content-Type': 'application/json' }

const toPayload = (b) => ({
  title: b.title,
  author: b.author,
  status: b.status,
  rating: b.rating ? Number(b.rating) : null,
})

export default function App() {
  const [books, setBooks] = useState([])
  const [form, setForm] = useState(EMPTY)
  const [error, setError] = useState('')

  async function load() {
    try {
      const res = await fetch(API)
      setBooks(await res.json())
    } catch {
      setError('Cannot reach the API')
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function addBook(e) {
    e.preventDefault()
    const res = await fetch(API, { method: 'POST', headers: JSON_HEADERS, body: JSON.stringify(toPayload(form)) })
    if (!res.ok) return setError('Could not save the book, check the fields')
    setForm(EMPTY)
    setError('')
    load()
  }

  async function changeStatus(book, status) {
    await fetch(`${API}/${book.id}`, { method: 'PUT', headers: JSON_HEADERS, body: JSON.stringify(toPayload({ ...book, status })) })
    load()
  }

  async function removeBook(id) {
    await fetch(`${API}/${id}`, { method: 'DELETE' })
    load()
  }

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  return (
    <main className="container">
      <h1>📚 Book Tracker v2</h1>
      <form className="card form" onSubmit={addBook}>
        <input placeholder="Title" required value={form.title} onChange={set('title')} />
        <input placeholder="Author" required value={form.author} onChange={set('author')} />
        <select value={form.status} onChange={set('status')}>
          {STATUSES.map((s) => <option key={s}>{s}</option>)}
        </select>
        <input type="number" min="1" max="5" placeholder="Rating 1-5" value={form.rating} onChange={set('rating')} />
        <button type="submit">Add book</button>
      </form>
      {error && <p className="error">{error}</p>}
      {books.length === 0 && <p className="muted">No books yet. Add your first one above.</p>}
      <ul className="list">
        {books.map((b) => (
          <li key={b.id} className="card item">
            <div>
              <strong>{b.title}</strong>
              <div className="muted">{b.author}{b.rating ? ` · ${'★'.repeat(b.rating)}` : ''}</div>
            </div>
            <div className="actions">
              <select value={b.status} onChange={(e) => changeStatus(b, e.target.value)}>
                {STATUSES.map((s) => <option key={s}>{s}</option>)}
              </select>
              <button className="danger" onClick={() => removeBook(b.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </main>
  )
}