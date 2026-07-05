import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const res = await api.post('/api/users/auth/login', form)
      login(res.data.access_token, res.data.user)
      navigate('/')
    } catch (err) {
      setError('Pogrešan email ili lozinka')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow w-full max-w-md">
        <h2 className="text-2xl font-bold text-indigo-600 mb-6">Prijava</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={e => setForm({...form, email: e.target.value})}
            className="w-full border rounded px-3 py-2"
            required
          />
          <input
            type="password"
            placeholder="Lozinka"
            value={form.password}
            onChange={e => setForm({...form, password: e.target.value})}
            className="w-full border rounded px-3 py-2"
            required
          />
          <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
            Prijavi se
          </button>
        </form>
        <p className="mt-4 text-center text-gray-600">
          Nemate nalog? <Link to="/register" className="text-indigo-600 hover:underline">Registrujte se</Link>
        </p>
      </div>
    </div>
  )
}