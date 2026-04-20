import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/auth_context';
import AppRoutes from './routes/app_routes';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
