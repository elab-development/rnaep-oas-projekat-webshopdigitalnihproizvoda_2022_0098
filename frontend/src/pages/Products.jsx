import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios'

export default function Products() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [search, setSearch] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [minPrice, setMinPrice] = useState('')
  const [maxPrice, setMaxPrice] = useState('')

  useEffect(() => {
    api.get('/api/products/categories').then(res => setCategories(res.data)).catch(() => {})
    fetchProducts()
  }, [])

  const fetchProducts = () => {
    const params = {}
    if (search) params.search = search
    if (categoryId) params.category_id = categoryId
    if (minPrice) params.min_price = minPrice
    if (maxPrice) params.max_price = maxPrice
    api.get('/api/products/', { params }).then(res => setProducts(res.data)).catch(() => {})
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-indigo-600 mb-6">Katalog proizvoda</h1>

      <div className="flex flex-wrap gap-3 mb-6">
        <input type="text" placeholder="Pretraži..." value={search}
          onChange={e => setSearch(e.target.value)}
          className="border rounded px-3 py-2 flex-1 min-w-48" />
        <select value={categoryId} onChange={e => setCategoryId(e.target.value)}
          className="border rounded px-3 py-2">
          <option value="">Sve kategorije</option>
          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <input type="number" placeholder="Min cena" value={minPrice}
          onChange={e => setMinPrice(e.target.value)}
          className="border rounded px-3 py-2 w-28" />
        <input type="number" placeholder="Max cena" value={maxPrice}
          onChange={e => setMaxPrice(e.target.value)}
          className="border rounded px-3 py-2 w-28" />
        <button onClick={fetchProducts}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
          Pretraži
        </button>
      </div>

      {products.length === 0 ? (
        <p className="text-gray-500">Nema proizvoda.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map(product => (
            <Link to={`/products/${product.id}`} key={product.id}
              className="bg-white rounded-lg shadow hover:shadow-md transition overflow-hidden">
              {product.thumbnail_url && (
                <img src={product.thumbnail_url} alt={product.name}
                  className="w-full h-48 object-cover" />
              )}
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-1">{product.name}</h3>
                <p className="text-gray-500 text-sm mb-2 line-clamp-2">{product.description}</p>
                <p className="text-indigo-600 font-bold">{product.price} RSD</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}