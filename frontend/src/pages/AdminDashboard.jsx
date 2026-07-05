import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

export default function AdminDashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [users, setUsers] = useState([])
  const [categories, setCategories] = useState([])
  const [newCategory, setNewCategory] = useState({ name: '', description: '' })
  const [message, setMessage] = useState('')
  const [activeTab, setActiveTab] = useState('users')

  useEffect(() => {
    if (!user || user.role !== 'admin') {
      navigate('/')
      return
    }
    fetchUsers()
    fetchCategories()
  }, [user])

  const fetchUsers = () => {
    api.get('/api/users/').then(res => setUsers(res.data)).catch(() => {})
  }

  const fetchCategories = () => {
    api.get('/api/products/categories').then(res => setCategories(res.data)).catch(() => {})
  }

  const handleDeactivate = async (userId) => {
    try {
      await api.put(`/api/users/${userId}/deactivate`)
      setMessage('Nalog uspešno deaktiviran')
      fetchUsers()
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Greška')
    }
  }

  const handleCreateCategory = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/products/categories', newCategory)
      setMessage('Kategorija uspešno kreirana')
      setNewCategory({ name: '', description: '' })
      fetchCategories()
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Greška')
    }
  }

  const handleDeleteCategory = async (categoryId) => {
    try {
      await api.delete(`/api/products/categories/${categoryId}`)
      setMessage('Kategorija uspešno obrisana')
      fetchCategories()
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Greška')
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-indigo-600 mb-6">Admin Dashboard</h1>

      {message && (
        <div className={`p-3 rounded mb-4 ${message.includes('Greška') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {message}
        </div>
      )}

      {/* Tabovi */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setActiveTab('users')}
          className={`px-4 py-2 rounded ${activeTab === 'users' ? 'bg-indigo-600 text-white' : 'bg-white border'}`}>
          Korisnici ({users.length})
        </button>
        <button
          onClick={() => setActiveTab('categories')}
          className={`px-4 py-2 rounded ${activeTab === 'categories' ? 'bg-indigo-600 text-white' : 'bg-white border'}`}>
          Kategorije ({categories.length})
        </button>
      </div>

      {/* Korisnici */}
      {activeTab === 'users' && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left px-4 py-3 text-gray-600">Ime</th>
                <th className="text-left px-4 py-3 text-gray-600">Email</th>
                <th className="text-left px-4 py-3 text-gray-600">Uloga</th>
                <th className="text-left px-4 py-3 text-gray-600">Status</th>
                <th className="text-left px-4 py-3 text-gray-600">Akcija</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {users.map(u => (
                <tr key={u.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">{u.first_name} {u.last_name}</td>
                  <td className="px-4 py-3 text-gray-600">{u.email}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      u.role === 'admin' ? 'bg-purple-100 text-purple-700' :
                      u.role === 'seller' ? 'bg-blue-100 text-blue-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {u.role}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${u.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                      {u.is_active ? 'Aktivan' : 'Neaktivan'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    {u.is_active && u.role !== 'admin' && (
                      <button
                        onClick={() => handleDeactivate(u.id)}
                        className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600">
                        Deaktiviraj
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Kategorije */}
      {activeTab === 'categories' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Kreiraj kategoriju</h2>
            <form onSubmit={handleCreateCategory} className="flex gap-3">
              <input
                type="text"
                placeholder="Naziv kategorije"
                value={newCategory.name}
                onChange={e => setNewCategory({...newCategory, name: e.target.value})}
                className="border rounded px-3 py-2 flex-1"
                required
              />
              <input
                type="text"
                placeholder="Opis (opciono)"
                value={newCategory.description}
                onChange={e => setNewCategory({...newCategory, description: e.target.value})}
                className="border rounded px-3 py-2 flex-1"
              />
              <button type="submit"
                className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
                Kreiraj
              </button>
            </form>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left px-4 py-3 text-gray-600">Naziv</th>
                  <th className="text-left px-4 py-3 text-gray-600">Opis</th>
                  <th className="text-left px-4 py-3 text-gray-600">Akcija</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {categories.map(c => (
                  <tr key={c.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium">{c.name}</td>
                    <td className="px-4 py-3 text-gray-600">{c.description || '—'}</td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => handleDeleteCategory(c.id)}
                        className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600">
                        Obriši
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}