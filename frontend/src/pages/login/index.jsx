import { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/use_auth';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login: authLogin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const registered = location.state?.registered ?? false;

  async function handle_submit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await authLogin(email, password);
      navigate('/feed');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <img src={logo} alt="OndeTá?" className="login-logo" />
        <p className="login-subtitle">Encontre seu pet perdido</p>

        {registered && (
          <p className="login-success">Usuário cadastrado com sucesso!</p>
        )}

        <form onSubmit={handle_submit} className="login-form">
          <div className="login-field">
            <label htmlFor="email">E-mail</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              required
              autoComplete="email"
            />
          </div>

          <div className="login-field">
            <label htmlFor="password">Senha</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              autoComplete="current-password"
            />
          </div>

          {error && <p className="login-error">{error}</p>}

          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <p className="login-register">
          Não tem conta?{' '}
          <Link to="/cadastro">Cadastre-se</Link>
        </p>
      </div>
    </div>
  );
}
