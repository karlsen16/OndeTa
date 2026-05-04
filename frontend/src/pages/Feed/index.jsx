import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5000';

const STATUS_LABEL = {
  lost: 'Perdido',
  found: 'Encontrado',
};

function PetCard({ pet, onDelete }) {
  const [deleting, setDeleting] = useState(false);

  async function handle_delete() {
    setDeleting(true);
    await onDelete(pet.id);
    setDeleting(false);
  }

  return (
    <div className="feed-card">
      <div className="feed-card-header">
        <span className={`feed-badge feed-badge--${pet.status}`}>
          {STATUS_LABEL[pet.status] ?? pet.status}
        </span>
        {pet.type && <span className="feed-card-type">{pet.type}</span>}
      </div>
      <h3 className="feed-card-name">{pet.name}</h3>
      {pet.description && (
        <p className="feed-card-description">{pet.description}</p>
      )}
      {pet.date && (
        <p className="feed-card-date">
          {new Date(pet.date).toLocaleDateString('pt-BR')}
        </p>
      )}
      {onDelete && (
        <button
          className="feed-card-delete-btn"
          onClick={handle_delete}
          disabled={deleting}
        >
          {deleting ? 'Excluindo...' : 'Excluir postagem'}
        </button>
      )}
    </div>
  );
}

export default function Feed() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [pets, setPets] = useState([]);
  const [myPets, setMyPets] = useState([]);
  const [error, setError] = useState('');
  const [myPostsError, setMyPostsError] = useState('');
  const [loading, setLoading] = useState(true);
  const [myPostsLoading, setMyPostsLoading] = useState(false);
  const [showMyPosts, setShowMyPosts] = useState(location.state?.showMyPosts ?? false);

  useEffect(() => {
    fetch_pets();
    if (location.state?.showMyPosts) {
      fetch_my_pets();
    }
  }, []);

  async function fetch_pets() {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/pets`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? 'Erro ao carregar pets');
      }

      setPets(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function fetch_my_pets() {
    setMyPostsLoading(true);
    setMyPostsError('');

    try {
      const response = await fetch(`${API_URL}/pets?user_id=${user.id}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? 'Erro ao carregar suas postagens');
      }

      setMyPets(data);
    } catch (err) {
      setMyPostsError(err.message);
    } finally {
      setMyPostsLoading(false);
    }
  }

  async function handle_delete(petId) {
    try {
      const response = await fetch(`${API_URL}/pets/${petId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error ?? 'Erro ao excluir postagem');
      }

      setMyPets((prev) => prev.filter((p) => p.id !== petId));
      setPets((prev) => prev.filter((p) => p.id !== petId));
    } catch (err) {
      setMyPostsError(err.message);
    }
  }

  function handle_toggle_my_posts() {
    if (!showMyPosts) {
      fetch_my_pets();
    }
    setShowMyPosts((prev) => !prev);
  }

  function handle_logout() {
    logout();
    navigate('/login');
  }

  return (
    <div className="feed-container">
      <header className="feed-header">
        <img src={logo} alt="OndeTá?" className="feed-logo" />
        <div className="feed-header-actions">
          <button
            className={!showMyPosts ? 'feed-nav-btn feed-nav-btn--active' : 'feed-nav-btn'}
            onClick={() => setShowMyPosts(false)}
          >
            Feed
          </button>
          <button
            className={showMyPosts ? 'feed-nav-btn feed-nav-btn--active' : 'feed-nav-btn'}
            onClick={handle_toggle_my_posts}
          >
            Minhas postagens
          </button>
          <button className="feed-nav-btn" onClick={() => navigate('/profile')}>
            Meu perfil
          </button>
          <button className="feed-logout-btn" onClick={handle_logout}>
            Sair
          </button>
        </div>
      </header>

      {showMyPosts ? (
        <main className="feed-main">
          <h2 className="feed-title">Minhas postagens</h2>

          {myPostsLoading && <p className="feed-loading">Carregando...</p>}
          {myPostsError && <p className="feed-error">{myPostsError}</p>}

          {!myPostsLoading && !myPostsError && myPets.length === 0 && (
            <p className="feed-empty">Você ainda não fez nenhuma postagem.</p>
          )}

          <div className="feed-grid">
            {myPets.map((pet) => (
              <PetCard key={pet.id} pet={pet} onDelete={handle_delete} />
            ))}
          </div>
        </main>
      ) : (
        <main className="feed-main">
          <h2 className="feed-title">Pets reportados</h2>

          {loading && <p className="feed-loading">Carregando...</p>}
          {error && <p className="feed-error">{error}</p>}

          {!loading && !error && pets.length === 0 && (
            <p className="feed-empty">Nenhum pet reportado ainda.</p>
          )}

          <div className="feed-grid">
            {pets.map((pet) => (
              <PetCard key={pet.id} pet={pet} onDelete={null} />
            ))}
          </div>
        </main>
      )}
    </div>
  );
}