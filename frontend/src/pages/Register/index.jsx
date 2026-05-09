import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [contact, setContact] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login: authLogin } = useAuth();
  const navigate = useNavigate();

  function format_contact(value) {
    const digits = value.replace(/\D/g, '').slice(0, 11);
    if (digits.length <= 10) {
      return digits
        .replace(/^(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d)/, '$1-$2');
    }
    return digits
      .replace(/^(\d{2})(\d)/, '($1) $2')
      .replace(/(\d{5})(\d)/, '$1-$2');
  }

  async function handle_submit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await api.post('/auth/register', {
        name,
        email,
        password,
        contact
      });

      await authLogin(email, password);

      navigate('/feed');

    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Erro ao processar cadastro';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="register-container">
      <div className="register-card">
        <img src={logo} alt="OndeTá?" className="register-logo" />
        <p className="register-subtitle">Crie sua conta</p>

        <form onSubmit={handle_submit} className="register-form">
          <div className="register-field">
            <label htmlFor="name">Nome</label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Seu nome completo"
              required
            />
          </div>

          <div className="register-field">
            <label htmlFor="email">E-mail</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              required
            />
          </div>

          <div className="register-field">
            <label htmlFor="password">Senha</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <div className="register-field">
            <label htmlFor="contact">
              Telefone <span className="register-optional">(opcional)</span>
            </label>
            <input
              id="contact"
              type="tel"
              value={contact}
              onChange={(e) => setContact(format_contact(e.target.value))}
              placeholder="(00) 00000-0000"
            />
          </div>

          {error && <p className="register-error">{error}</p>}

          <button type="submit" className="register-btn" disabled={loading}>
            {loading ? 'Processando...' : 'Criar conta'}
          </button>
        </form>

        <p className="register-link">
          Já tem conta?{' '}
          <Link to="/login">Entrar</Link>
        </p>
      </div>
    </div>
  );
}