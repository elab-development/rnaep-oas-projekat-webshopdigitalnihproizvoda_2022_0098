import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function Notifications() {
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    api.get('/api/notifications/').then(res => setNotifications(res.data)).catch(() => {})
  }, [])

  const markAsRead = async (id) => {
    await api.put(`/api/notifications/${id}/read`)
    setNotifications(notifications.map(n => n.id === id ? {...n, is_read: true} : n))
  }

  const markAllAsRead = async () => {
    await api.put('/api/notifications/read-all')
    setNotifications(notifications.map(n => ({...n, is_read: true})))
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-indigo-600">Notifikacije</h1>
        <button onClick={markAllAsRead} className="text-sm text-indigo-600 hover:underline">
          Označi sve kao pročitano
        </button>
      </div>

      {notifications.length === 0 ? (
        <p className="text-gray-500">Nema notifikacija.</p>
      ) : (
        <div className="space-y-3">
          {notifications.map(n => (
            <div key={n.id}
              className={`bg-white rounded-lg shadow p-4 flex justify-between items-start ${!n.is_read ? 'border-l-4 border-indigo-600' : ''}`}>
              <div>
                <p className="font-semibold">{n.title}</p>
                <p className="text-gray-600 text-sm">{n.message}</p>
                <p className="text-gray-400 text-xs mt-1">{new Date(n.created_at).toLocaleString()}</p>
              </div>
              {!n.is_read && (
                <button onClick={() => markAsRead(n.id)}
                  className="text-xs text-indigo-600 hover:underline ml-4 whitespace-nowrap">
                  Označi kao pročitano
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}