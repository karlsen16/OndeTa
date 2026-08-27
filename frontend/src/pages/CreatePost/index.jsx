import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

const PET_TYPES = [
  { value: 'cachorro', label: 'Cachorro' },
  { value: 'gato', label: 'Gato' },
];

export default function CreatePost() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [category, setCategory] = useState('');
  const [petName, setPetName] = useState('');
  const [petType, setPetType] = useState('');
  const [description, setDescription] = useState('');
  const [coords, setCoords] = useState(null);
  const [geoLoading, setGeoLoading] = useState(false);
  const [geoError, setGeoError] = useState('');
  const [submitError, setSubmitError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!user) navigate('/login');
  }, [user]);

  function handleUseLocation() {
    if (!navigator.geolocation) {
      setGeoError('Geolocalização não suportada pelo navegador');
      return;
    }
    setGeoLoading(true);
    setGeoError('');
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setCoords({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
        setGeoLoading(false);
      },
      () => {
        setGeoError('Não foi possível obter sua localização');
        setGeoLoading(false);
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 }
    );
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitError('');

    if (!coords) {
      setSubmitError('Use sua localização antes de publicar.');
      return;
    }

    setSubmitting(true);
    try {
      await api.post('/posts', {
        pet_name: petName || undefined,
        pet_type: petType,
        category,
        description: description || undefined,
        latitude: coords.latitude,
        longitude: coords.longitude,
      });

      navigate('/feed', { state: { showMyPosts: true } });
    } catch (err) {
      setSubmitError(
        err.response?.data?.message ?? err.response?.data?.error ?? 'Erro ao criar postagem'
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="create-post-container">
      <div className="create-post-card">
        <img src={logo} alt="OndeTá?" className="create-post-logo" />

        <h1 className="create-post-title">O que aconteceu?</h1>

        <div className="create-post-category-options">
          <button
            type="button"
            className={`create-post-category-btn ${category === 'perdido' ? 'create-post-category-btn--selected' : ''}`}
            onClick={() => setCategory('perdido')}
          >
            🔍 Perdi um animal
          </button>
          <button
            type="button"
            className={`create-post-category-btn ${category === 'encontrado' ? 'create-post-category-btn--selected' : ''}`}
            onClick={() => setCategory('encontrado')}
          >
            🐾 Encontrei um animal
          </button>
        </div>

        {category && (
          <form onSubmit={handleSubmit} className="create-post-form">
            <div className="create-post-field">
              <label htmlFor="petName">
                Nome do animal <span className="create-post-optional">(opcional)</span>
              </label>
              <input
                id="petName"
                type="text"
                value={petName}
                onChange={(e) => setPetName(e.target.value)}
                placeholder="Ex: Rex"
              />
            </div>

            <div className="create-post-field">
              <label htmlFor="petType">Tipo</label>
              <select
                id="petType"
                value={petType}
                onChange={(e) => setPetType(e.target.value)}
                required
              >
                <option value="">Selecione</option>
                {PET_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
            </div>

            <div className="create-post-field">
              <label htmlFor="description">
                Descrição <span className="create-post-optional">(opcional)</span>
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Características do animal, local onde foi visto..."
                rows={4}
              />
            </div>

            <div className="create-post-field">
              <label>Localização</label>
              <button
                type="button"
                className="create-post-geo-btn"
                onClick={handleUseLocation}
                disabled={geoLoading}
              >
                {geoLoading ? 'Obtendo localização...' : coords ? 'Localização obtida ✓' : 'Usar minha localização'}
              </button>
              {geoError && <p className="create-post-error">{geoError}</p>}
            </div>

            {submitError && <p className="create-post-error">{submitError}</p>}

            <button type="submit" className="create-post-submit-btn" disabled={submitting}>
              {submitting ? 'Publicando...' : 'Publicar postagem'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
