import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5000';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [contact, setPhone] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

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
      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: name, email, senha: password, telefone: contact || undefined }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? 'Erro ao criar conta');
      }

      navigate('/login', { state: { registered: true } });
    } catch (err) {
      setError(err.message);
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
              autoComplete="name"
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
              autoComplete="email"
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
              autoComplete="new-password"
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
              onChange={(e) => setPhone(format_contact(e.target.value))}
              placeholder="(00) 00000-0000"
              autoComplete="tel"
            />
          </div>

          {error && <p className="register-error">{error}</p>}

          <button type="submit" className="register-btn" disabled={loading}>
            {loading ? 'Criando conta...' : 'Criar conta'}
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