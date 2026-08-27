import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

const STATUS_LABEL = {
  perdido: 'Perdido',
  encontrado: 'Encontrado',
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
        <span className={`feed-badge feed-badge--${pet.category}`}>
          {STATUS_LABEL[pet.category] ?? pet.category}
        </span>
        {pet.pet_type && <span className="feed-card-type">{pet.pet_type}</span>}
      </div>
      <h3 className="feed-card-name">{pet.pet_name}</h3>
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
      const response = await api.get('/posts');
      setPets(response.data.posts);
    } catch (err) {
      setError(err.response?.data?.message || 'Erro ao carregar pets');
    } finally {
      setLoading(false);
    }
  }

  async function fetch_my_pets() {
    setMyPostsLoading(true);
    setMyPostsError('');
    try {
      const response = await api.get('/posts', {
        params: { limit: 100 }
      });
      setMyPets(response.data.posts.filter((p) => p.author?.id === user.id));
    } catch (err) {
      setMyPostsError(err.response?.data?.message || 'Erro ao carregar suas postagens');
    } finally {
      setMyPostsLoading(false);
    }
  }

  async function handle_delete(petId) {
    try {
      await api.delete(`/pets/${petId}`, {
        data: { user_id: user.id }
      });

      setMyPets((prev) => prev.filter((p) => p.id !== petId));
      setPets((prev) => prev.filter((p) => p.id !== petId));
    } catch (err) {
      setMyPostsError(err.response?.data?.error || 'Erro ao excluir postagem');
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
          <button className="feed-nav-btn" onClick={() => navigate('/create-post')}>
            Criar postagem
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