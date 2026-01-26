import { Outlet } from 'react-router-dom'

function Layout() {
  return (
    <div className="min-h-screen bg-white">
      <nav className="bg-black shadow-sm border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold text-white">
                ◆ CodeGuard
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-300">Dashboard</span>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
