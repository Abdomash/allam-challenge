import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { LandingPage } from './pages/LandingPage.tsx'
import NotFoundPage from './NotFoundPage.tsx'
import './index.css'

const router = createBrowserRouter([
  {
    path: '/',
    element: <LandingPage />,
    errorElement: <NotFoundPage />,
  },
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
