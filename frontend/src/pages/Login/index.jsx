import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [carregando, setCarregando] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setCarregando(true);

    try {
      await login(email, password);
      navigate('/feed');
    } catch (err) {
      setError(err.message);
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <img src={logo} alt="OndeTá?" className="login-logo" />
        <p className="login-subtitle">Encontre seu pet perdido</p>

        <form onSubmit={handleSubmit} className="login-form">
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
            <label htmlFor="senha">Senha</label>
            <input
              id="senha"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              autoComplete="current-password"
            />
          </div>

          {error && <p className="login-erro">{error}</p>}

          <button type="submit" className="login-btn" disabled={carregando}>
            {carregando ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <p className="login-cadastro">
          Não tem conta?{' '}
          <Link to="/cadastro">Cadastre-se</Link>
        </p>
      </div>
    </div>
  );
}
