import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'

export default function ProductDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [product, setProduct] = useState(null)
  const [prices, setPrices] = useState(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.get(`/api/products/${id}`).then(res => {
      setProduct(res.data)
      return api.get(`/api/orders/exchange/${res.data.price}`)
    }).then(res => setPrices(res.data)).catch(() => {})
  }, [id])

  const handleBuy = async () => {
    if (!user) { navigate('/login'); return }
    setLoading(true)
    try {
      await api.post('/api/orders/', { product_id: id })
      setMessage('Kupovina uspešna! Pogledajte vaše kupovine.')
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Greška pri kupovini')
    }
    setLoading(false)
  }

  if (!product) return <div className="text-center py-8">Učitavanje...</div>

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {product.thumbnail_url && (
        <img src={product.thumbnail_url} alt={product.name}
          className="w-full h-64 object-cover rounded-lg mb-6" />
      )}
      <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
      <p className="text-gray-600 mb-4">{product.description}</p>

      {prices && (
        <div className="bg-gray-50 rounded-lg p-4 mb-4">
          <h3 className="font-semibold mb-2">Cena u valutama:</h3>
          <div className="flex gap-6">
            <span className="text-indigo-600 font-bold">{prices.RSD} RSD</span>
            <span className="text-green-600 font-bold">{prices.EUR} EUR</span>
            <span className="text-blue-600 font-bold">{prices.USD} USD</span>
          </div>
        </div>
      )}

      {message && (
        <div className={`p-3 rounded mb-4 ${message.includes('uspešna') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {message}
        </div>
      )}

      {user?.role === 'buyer' && (
        <button onClick={handleBuy} disabled={loading}
          className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 disabled:opacity-50">
          {loading ? 'Obrađuje se...' : 'Kupi odmah'}
        </button>
      )}
    </div>
  )
}