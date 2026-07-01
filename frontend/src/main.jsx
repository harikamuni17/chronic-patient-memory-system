import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import App from './App';
import './styles/global.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#0d1628',
            color: '#f1f5f9',
            border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: '0.75rem',
            fontSize: '0.875rem',
            boxShadow: '0 8px 40px rgba(0,0,0,0.6)',
          },
          success: { iconTheme: { primary: '#10b981', secondary: '#0d1628' } },
          error:   { iconTheme: { primary: '#ef4444', secondary: '#0d1628' } },
        }}
      />
    </BrowserRouter>
  </React.StrictMode>
);
