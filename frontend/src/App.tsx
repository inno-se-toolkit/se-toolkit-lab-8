import { useState, useEffect, useReducer, FormEvent } from 'react'
import Dashboard from './Dashboard'
import './App.css'

const STORAGE_KEY = 'api_key'

type Page = 'items' | 'dashboard'

interface Item {
  id: number
  type: string
  title: string
  created_at: string
}

type FetchState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; items: Item[] }
  | { status: 'error'; message: string }

type FetchAction =
  | { type: 'fetch_start' }
  | { type: 'fetch_success'; data: Item[] }
  | { type: 'fetch_error'; message: string }

function fetchReducer(_state: FetchState, action: FetchAction): FetchState {
  switch (action.type) {
    case 'fetch_start':
      return { status: 'loading' }
    case 'fetch_success':
      return { status: 'success', items: action.data }
    case 'fetch_error':
      return { status: 'error', message: action.message }
  }
}

function App() {
  const [token, setToken] = useState(
    () => localStorage.getItem(STORAGE_KEY) ?? '',
  )
  const [draft, setDraft] = useState('')
  const [page, setPage] = useState<Page>('items')
  const [fetchState, dispatch] = useReducer(fetchReducer, { status: 'idle' })

  useEffect(() => {
    if (!token) return

    dispatch({ type: 'fetch_start' })

    fetch('/items/', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((data: Item[]) => dispatch({ type: 'fetch_success', data }))
      .catch((err: Error) =>
        dispatch({ type: 'fetch_error', message: err.message }),
      )
  }, [token])

  function handleConnect(e: FormEvent) {
    e.preventDefault()
    const trimmed = draft.trim()
    if (!trimmed) return
    localStorage.setItem(STORAGE_KEY, trimmed)
    setToken(trimmed)
  }

  function handleDisconnect() {
    localStorage.removeItem(STORAGE_KEY)
    setToken('')
    setDraft('')
  }

  if (!token) {
    return (
      <form className="token-form" onSubmit={handleConnect}>
        <h1>LMS API Key</h1>
        <p>Enter your LMS API key to connect.</p>
        <input
          type="password"
          placeholder="Token"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
        />
        <button type="submit">Connect</button>
      </form>
    )
  }

  return (
    <div>
      <header className="app-header">
        <nav className="nav-links">
          <button
            className={page === 'items' ? 'nav-active' : ''}
            onClick={() => setPage('items')}
          >
            Items
          </button>
          <button
            className={page === 'dashboard' ? 'nav-active' : ''}
            onClick={() => setPage('dashboard')}
          >
            Dashboard
          </button>
        </nav>
        <button className="btn-disconnect" onClick={handleDisconnect}>
          Disconnect
        </button>
      </header>

      {page === 'dashboard' ? (
        <Dashboard token={token} />
      ) : (
        <>
          {fetchState.status === 'loading' && <p>Loading...</p>}
          {fetchState.status === 'error' && <p>Error: {fetchState.message}</p>}

          {fetchState.status === 'success' && (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>ItemType</th>
                  <th>Title</th>
                  <th>Created at</th>
                </tr>
              </thead>
              <tbody>
                {fetchState.items.map((item) => (
                  <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>{item.type}</td>
                    <td>{item.title}</td>
                    <td>{item.created_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  )
}

export default App
