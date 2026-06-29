import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios'

export default function MyProducts() {
  const [products, setProducts] = useState([])
  const [stats, setStats] = useState([])
  const [form, setForm] = useState({ name: '', description: '', price: '', category_id: '', file_path: '' })
  const [message, setMessage] = useState('')

  useEffect(() => {
    api.get('/api/products/seller/my-products').then(res => setProducts(res.data)).catch(() => {})
    api.get('/api/orders/seller/stats').then(res => setStats(res.data)).catch(() => {})
  }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/products/', form)
      setMessage('Proizvod uspešno kreiran!')
      api.get('/api/products/seller/my-products').then(res => setProducts(res.data))
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Greška')
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-indigo-600 mb-6">Moji proizvodi</h1>

      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Kreiraj novi proizvod</h2>
        {message && <p className="text-green-600 mb-4">{message}</p>}
        <form onSubmit={handleCreate} className="space-y-3">
          <input type="text" placeholder="Naziv" value={form.name}
            onChange={e => setForm({...form, name: e.target.value})}
            className="w-full border rounded px-3 py-2" required />
          <textarea placeholder="Opis" value={form.description}
            onChange={e => setForm({...form, description: e.target.value})}
            className="w-full border rounded px-3 py-2" rows={3} required />
          <input type="number" placeholder="Cena (RSD)" value={form.price}
            onChange={e => setForm({...form, price: e.target.value})}
            className="w-full border rounded px-3 py-2" required />
          <input type="text" placeholder="Putanja do fajla (npr. /files/kurs.pdf)" value={form.file_path}
            onChange={e => setForm({...form, file_path: e.target.value})}
            className="w-full border rounded px-3 py-2" required />
          <button type="submit" className="bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700">
            Kreiraj proizvod
          </button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Statistika prodaje</h2>
        {stats.length === 0 ? <p className="text-gray-500">Još uvek nema prodaja.</p> : (
          <div className="space-y-2">
            {stats.map(s => (
              <div key={s.product_id} className="flex justify-between border-b pb-2">
                <span className="text-gray-600">Proizvod #{s.product_id.slice(0, 8)}</span>
                <span>{s.total_sales} prodaja — {s.total_revenue} RSD</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <h2 className="text-xl font-semibold mb-4">Svi moji proizvodi</h2>
      {products.length === 0 ? <p className="text-gray-500">Nemate proizvoda.</p> : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {products.map(p => (
            <div key={p.id} className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold">{p.name}</h3>
              <p className="text-indigo-600 font-bold">{p.price} RSD</p>
              <p className={`text-sm ${p.is_active ? 'text-green-600' : 'text-red-600'}`}>
                {p.is_active ? 'Aktivan' : 'Neaktivan'}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}