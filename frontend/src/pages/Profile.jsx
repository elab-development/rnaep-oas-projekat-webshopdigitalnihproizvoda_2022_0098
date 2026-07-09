import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'

export default function Profile() {
  const { user, login, token } = useAuth()
  const [form, setForm] = useState({ first_name: '', last_name: '' })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    if (user) {
      setForm({ first_name: user.first_name, last_name: user.last_name })
    }
  }, [user])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage('')
    setError('')
    try {
      const res = await api.put('/api/users/me', form)
      login(token, res.data)
      setMessage('Podaci uspešno ažurirani!')
    } catch (err) {
      setError(err.response?.data?.detail || 'Greška pri ažuriranju')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow w-full max-w-md">
        <h2 className="text-2xl font-bold text-indigo-600 mb-6">Moj profil</h2>
        <div className="mb-4 p-3 bg-gray-50 rounded">
          <p className="text-sm text-gray-500">Email</p>
          <p className="font-medium">{user?.email}</p>
        </div>
        <div className="mb-6 p-3 bg-gray-50 rounded">
          <p className="text-sm text-gray-500">Uloga</p>
          <p className="font-medium">{user?.role}</p>
        </div>
        {message && <p className="text-green-600 mb-4">{message}</p>}
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-600 mb-1">Ime</label>
            <input
              type="text"
              value={form.first_name}
              onChange={e => setForm({...form, first_name: e.target.value})}
              className="w-full border rounded px-3 py-2"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Prezime</label>
            <input
              type="text"
              value={form.last_name}
              onChange={e => setForm({...form, last_name: e.target.value})}
              className="w-full border rounded px-3 py-2"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
            Sačuvaj izmene
          </button>
        </form>
      </div>
    </div>
  )
}