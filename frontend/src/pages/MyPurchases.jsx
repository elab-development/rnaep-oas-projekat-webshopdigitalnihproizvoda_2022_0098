import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function MyPurchases() {
  const [orders, setOrders] = useState([])

  useEffect(() => {
    api.get('/api/orders/my-purchases').then(res => setOrders(res.data)).catch(() => {})
  }, [])

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-indigo-600 mb-6">Moje kupovine</h1>
      {orders.length === 0 ? (
        <p className="text-gray-500">Nemate kupovina.</p>
      ) : (
        <div className="space-y-4">
          {orders.map(order => (
            <div key={order.id} className="bg-white rounded-lg shadow p-4 flex justify-between items-center">
              <div>
                <p className="font-semibold">Narudžbina #{order.id.slice(0, 8)}</p>
                <p className="text-gray-500 text-sm">Status: <span className={`font-medium ${order.status === 'confirmed' ? 'text-green-600' : 'text-red-600'}`}>{order.status}</span></p>
                <p className="text-indigo-600 font-bold">{order.amount} RSD</p>
              </div>
              {order.status === 'confirmed' && (
                <button
                  onClick={() => api.get(`/api/orders/${order.id}/download`).then(res => alert(`Download token: ${res.data.download_token}`))}
                  className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
                  Preuzmi
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}