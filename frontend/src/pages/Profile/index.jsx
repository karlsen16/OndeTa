import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

export default function Profile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [passwordSuccess, setPasswordSuccess] = useState('');
  const [passwordLoading, setPasswordLoading] = useState(false);

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetch_profile();
  }, [user]);

  async function fetch_profile() {
    try {
      const response = await api.get('/me');
      setProfile(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Erro ao carregar perfil');
    } finally {
      setLoading(false);
    }
  }

  async function handle_update_password(e) {
    e.preventDefault();
    setPasswordError('');
    setPasswordSuccess('');

    if (newPassword !== confirmPassword) {
      setPasswordError('As senhas não coincidem');
      return;
    }

    if (newPassword.length < 6) {
      setPasswordError('A nova senha deve ter pelo menos 6 caracteres');
      return;
    }

    setPasswordLoading(true);

    try {
      await api.patch('/me/password', {
        old_password: currentPassword,
        new_password: newPassword
      });

      setPasswordSuccess('Senha atualizada com sucesso!');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err) {
      setPasswordError(err.response?.data?.message || err.response?.data?.error || 'Erro ao redefinir senha');
    } finally {
      setPasswordLoading(false);
    }
  }

  async function handle_delete_account() {
    setDeleteLoading(true);
    setDeleteError('');

    try {
      await api.delete(`/users/${user.id}`);

      logout();
      navigate('/register');
    } catch (err) {
      setDeleteError(err.response?.data?.error || 'Erro ao excluir conta');
      setDeleteLoading(false);
    }
  }

  function handle_logout() {
    logout();
    navigate('/login');
  }

  return (
    <div className="profile-container">
      <header className="profile-header">
        <img src={logo} alt="OndeTá?" className="profile-header-logo" />
        <div className="profile-header-actions">
          <button className="profile-header-btn" onClick={() => navigate('/feed')}>
            Feed
          </button>
          <button className="profile-header-btn" onClick={() => navigate('/feed', { state: { showMyPosts: true } })}>
            Minhas postagens
          </button>
          <button className="profile-header-btn" onClick={() => navigate('/create-post')}>
            Criar postagem
          </button>
          <button className="profile-header-btn profile-header-btn--active">
            Meu perfil
          </button>
          <button className="profile-header-btn profile-header-btn--logout" onClick={handle_logout}>
            Sair
          </button>
        </div>
      </header>

      <main className="profile-main">
        <div className="profile-card">
          <p className="profile-subtitle">Meu perfil</p>

          {loading && <p className="profile-loading">Carregando...</p>}
          {error && <p className="profile-error">{error}</p>}

          {profile && (
            <div className="profile-info">
              <div className="profile-field">
                <span className="profile-label">Nome</span>
                <span className="profile-value">{profile.name}</span>
              </div>
              <div className="profile-field">
                <span className="profile-label">E-mail</span>
                <span className="profile-value">{profile.email}</span>
              </div>
              {profile.contact && (
                <div className="profile-field">
                  <span className="profile-label">Telefone</span>
                  <span className="profile-value">{profile.contact}</span>
                </div>
              )}
            </div>
          )}

          <div className="profile-actions">
            <button
              className="profile-btn profile-btn--secondary"
              onClick={() => { setShowPasswordForm((v) => !v); setShowDeleteConfirm(false); }}
            >
              Redefinir senha
            </button>

            <button
              className="profile-btn profile-btn--danger-outline"
              onClick={() => { setShowDeleteConfirm((v) => !v); setShowPasswordForm(false); }}
            >
              Excluir conta
            </button>
          </div>

          {showPasswordForm && (
            <form className="profile-form" onSubmit={handle_update_password}>
              <p className="profile-form-title">Redefinir senha</p>

              {passwordSuccess && <p className="profile-success">{passwordSuccess}</p>}
              {passwordError && <p className="profile-error">{passwordError}</p>}

              <div className="profile-form-field">
                <label htmlFor="current_password">Senha atual</label>
                <input
                  id="current_password"
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                />
              </div>

              <div className="profile-form-field">
                <label htmlFor="new_password">Nova senha</label>
                <input
                  id="new_password"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                />
              </div>

              <div className="profile-form-field">
                <label htmlFor="confirm_password">Confirmar nova senha</label>
                <input
                  id="confirm_password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                />
              </div>

              <button type="submit" className="profile-btn" disabled={passwordLoading}>
                {passwordLoading ? 'Salvando...' : 'Salvar nova senha'}
              </button>
            </form>
          )}

          {showDeleteConfirm && (
            <div className="profile-delete-confirm">
              <p className="profile-delete-text">
                Tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita.
              </p>
              {deleteError && <p className="profile-error">{deleteError}</p>}
              <div className="profile-delete-btns">
                <button
                  className="profile-btn profile-btn--danger"
                  onClick={handle_delete_account}
                  disabled={deleteLoading}
                >
                  {deleteLoading ? 'Excluindo...' : 'Sim, excluir conta'}
                </button>
                <button
                  className="profile-btn profile-btn--secondary"
                  onClick={() => setShowDeleteConfirm(false)}
                >
                  Cancelar
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}