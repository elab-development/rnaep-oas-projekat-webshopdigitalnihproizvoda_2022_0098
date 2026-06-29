import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Home() {
  const { user } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-4xl font-bold text-indigo-600 mb-4">
        Dobrodošli na Digital Marketplace
      </h1>
      <p className="text-gray-600 text-lg mb-8 max-w-xl">
        Platforma za kupovinu i prodaju digitalnih proizvoda — kursevi, e-knjige, template-i i još mnogo toga.
      </p>
      <div className="flex gap-4">
        <Link to="/products" className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700">
          Pretraži proizvode
        </Link>
        {!user && (
          <Link to="/register" className="border border-indigo-600 text-indigo-600 px-6 py-3 rounded-lg hover:bg-indigo-50">
            Registruj se
          </Link>
        )}
      </div>
    </div>
  )
}