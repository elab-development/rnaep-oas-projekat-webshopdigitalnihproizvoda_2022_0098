import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useState, useEffect } from 'react'
import api from '../api/axios'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [unreadCount, setUnreadCount] = useState(0)

  useEffect(() => {
    if (user) {
      api.get('/api/notifications/unread-count')
        .then(res => setUnreadCount(res.data.unread_count))
        .catch(() => {})
    }
  }, [user])

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="bg-indigo-600 text-white px-6 py-4 flex justify-between items-center">
      <Link to="/" className="text-xl font-bold">Digital Marketplace</Link>
      <div className="flex items-center gap-4">
        <Link to="/products" className="hover:underline">Proizvodi</Link>
        {user ? (
          <>
            {user.role === 'seller' && (
              <Link to="/my-products" className="hover:underline">Moji proizvodi</Link>
            )}
            {user.role === 'admin' && (
              <Link to="/admin" className="hover:underline">Admin Panel</Link>
            )}
            {user.role === 'buyer' && (
              <Link to="/my-purchases" className="hover:underline">Moje kupovine</Link>
            )}
            <Link to="/notifications" className="relative hover:underline">
              🔔
              {unreadCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </Link>
            <span className="text-sm">{user.first_name}</span>
            <button onClick={handleLogout} className="bg-white text-indigo-600 px-3 py-1 rounded hover:bg-gray-100">
              Odjavi se
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:underline">Prijava</Link>
            <Link to="/register" className="bg-white text-indigo-600 px-3 py-1 rounded hover:bg-gray-100">
              Registracija
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}