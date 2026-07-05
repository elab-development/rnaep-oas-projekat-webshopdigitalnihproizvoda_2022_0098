import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'

export default function Register() {
  const [form, setForm] = useState({
    first_name: '', last_name: '', email: '', password: '', role: 'buyer'
  })
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const res = await api.post('/api/users/auth/register', form)
      login(res.data.access_token, res.data.user)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Greška pri registraciji')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow w-full max-w-md">
        <h2 className="text-2xl font-bold text-indigo-600 mb-6">Registracija</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input type="text" placeholder="Ime" value={form.first_name}
            onChange={e => setForm({...form, first_name: e.target.value})}
            className="w-full border rounded px-3 py-2" required />
          <input type="text" placeholder="Prezime" value={form.last_name}
            onChange={e => setForm({...form, last_name: e.target.value})}
            className="w-full border rounded px-3 py-2" required />
          <input type="email" placeholder="Email" value={form.email}
            onChange={e => setForm({...form, email: e.target.value})}
            className="w-full border rounded px-3 py-2" required />
          <input type="password" placeholder="Lozinka" value={form.password}
            onChange={e => setForm({...form, password: e.target.value})}
            className="w-full border rounded px-3 py-2" required />
          <select value={form.role} onChange={e => setForm({...form, role: e.target.value})}
            className="w-full border rounded px-3 py-2">
            <option value="buyer">Kupac</option>
            <option value="seller">Prodavac</option>
          </select>
          <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
            Registruj se
          </button>
        </form>
        <p className="mt-4 text-center text-gray-600">
          Već imate nalog? <Link to="/login" className="text-indigo-600 hover:underline">Prijavite se</Link>
        </p>
      </div>
    </div>
  )
}