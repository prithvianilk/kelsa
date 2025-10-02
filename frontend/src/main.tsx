import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import MyWorkPage from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MyWorkPage />
  </StrictMode>
)
