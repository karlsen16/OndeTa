import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import logo from '../../assets/Logo-ondeta-v1.png';
import './styles.css';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5000';
const NOMINATIM = 'https://nominatim.openstreetmap.org';
const IBGE = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios';
const GEO_HEADERS = { 'User-Agent': 'OndeTa/1.0' };

async function SearchCities(query, signal) {
  const res = await fetch(`${IBGE}?nome=${encodeURIComponent(query)}&orderBy=nome`, { signal });
  const data = await res.json();
  const lower = query.toLowerCase();
  return data
    .filter((m) => m.nome.toLowerCase().startsWith(lower))
    .slice(0, 6)
    .map((m) => ({
      value: m.nome,
      label: `${m.nome} - ${m.microrregiao.mesorregiao.UF.sigla}`,
    }));
}

async function SearchStreets(street, city, signal) {
  const res = await fetch(
    `https://photon.komoot.io/api/?q=${encodeURIComponent(`${street}, ${city}`)}&limit=15&lang=pt&bbox=-73.98,-33.75,-28.86,5.27`,
    { signal }
  );
  const data = await res.json();
  const roads = data.features
    .map((f) => f.properties?.street || f.properties?.name)
    .filter(Boolean);
  return [...new Set(roads)].slice(0, 6);
}

async function SearchNeighborhoods(street, city) {
  const res = await fetch(
    `${NOMINATIM}/search?street=${encodeURIComponent(street)}&city=${encodeURIComponent(city)}&country=Brazil&format=json&addressdetails=1&limit=20&countrycodes=br`,
    { headers: GEO_HEADERS }
  );
  const data = await res.json();
  const neighborhoods = data
    .map((r) => r.address?.suburb || r.address?.neighbourhood || r.address?.quarter)
    .filter(Boolean);
  return [...new Set(neighborhoods)];
}

async function GeocodeFullAddress(street, number, neighborhood, city) {
  const parts = [street, number, neighborhood, city, 'Brasil'].filter(Boolean);
  const res = await fetch(
    `${NOMINATIM}/search?q=${encodeURIComponent(parts.join(', '))}&format=json&limit=1&countrycodes=br`,
    { headers: GEO_HEADERS }
  );
  const data = await res.json();
  if (!data.length) return null;
  return { latitude: parseFloat(data[0].lat), longitude: parseFloat(data[0].lon) };
}

async function ReverseGeocode(lat, lon) {
  const res = await fetch(
    `${NOMINATIM}/reverse?lat=${lat}&lon=${lon}&format=json`,
    { headers: GEO_HEADERS }
  );
  const data = await res.json();
  const addr = data.address ?? {};
  return {
    city: addr.city || addr.town || addr.village || addr.municipality || '',
    street: addr.road || '',
    neighborhood: addr.suburb || addr.neighbourhood || addr.quarter || '',
    number: addr.house_number || '',
  };
}

export default function CreatePost() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [status, setStatus] = useState('');
  const [name, setName] = useState('');
  const [type, setType] = useState('');
  const [description, setDescription] = useState('');

  const [city, setCity] = useState('');
  const [cityOptions, setCityOptions] = useState([]);
  const [street, setStreet] = useState('');
  const [streetOptions, setStreetOptions] = useState([]);
  const [number, setNumber] = useState('');
  const [neighborhood, setNeighborhood] = useState('');
  const [neighborhoodOptions, setNeighborhoodOptions] = useState([]);
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);

  const [isLoading, setIsLoading] = useState(false);
  const [geoLoading, setGeoLoading] = useState(false);
  const [error, setError] = useState('');

  const cityDebounceRef = useRef(null);
  const cityAbortRef = useRef(null);
  const streetDebounceRef = useRef(null);
  const streetAbortRef = useRef(null);

  useEffect(() => {
    if (!user) navigate('/login');
  }, [user]);

  function HandleContinue() {
    setError('');
    setStep(2);
  }

  function HandleCityChange(e) {
    const value = e.target.value;
    setCity(value);
    setLatitude(null);
    setLongitude(null);
    setNeighborhoodOptions([]);
    clearTimeout(cityDebounceRef.current);
    if (cityAbortRef.current) cityAbortRef.current.abort();
    if (value.length < 2) { setCityOptions([]); return; }
    cityDebounceRef.current = setTimeout(async () => {
      cityAbortRef.current = new AbortController();
      try {
        const options = await SearchCities(value, cityAbortRef.current.signal);
        setCityOptions(options);
      } catch (err) {
        if (err.name !== 'AbortError') setCityOptions([]);
      }
    }, 150);
  }

  function HandleSelectCity(option) {
    setCity(option.value);
    setCityOptions([]);
    setStreetOptions([]);
    setNeighborhoodOptions([]);
  }

  function HandleStreetChange(e) {
    const value = e.target.value;
    setStreet(value);
    setNeighborhoodOptions([]);
    setLatitude(null);
    setLongitude(null);
    clearTimeout(streetDebounceRef.current);
    if (streetAbortRef.current) streetAbortRef.current.abort();
    if (value.length < 3 || !city) { setStreetOptions([]); return; }
    streetDebounceRef.current = setTimeout(async () => {
      streetAbortRef.current = new AbortController();
      try {
        const options = await SearchStreets(value, city, streetAbortRef.current.signal);
        setStreetOptions(options);
      } catch (err) {
        if (err.name !== 'AbortError') setStreetOptions([]);
      }
    }, 150);
  }

  function HandleSelectStreet(option) {
    setStreet(option);
    setStreetOptions([]);
    setNeighborhoodOptions([]);
  }

  async function HandleNeighborhoodFocus() {
    if (!street || !city || neighborhoodOptions.length > 0) return;
    const options = await SearchNeighborhoods(street, city);
    setNeighborhoodOptions(options);
  }

  function HandleSelectNeighborhood(option) {
    setNeighborhood(option);
    setNeighborhoodOptions([]);
  }

  async function HandleGeolocate() {
    if (!navigator.geolocation) {
      setError('Geolocalização não suportada pelo navegador');
      return;
    }
    setGeoLoading(true);
    setError('');
    try {
      const position = await new Promise((resolve, reject) =>
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: false,
          timeout: 10000,
          maximumAge: 300000,
        })
      );
      const { latitude: lat, longitude: lon } = position.coords;
      const addr = await ReverseGeocode(lat, lon);
      setCity(addr.city);
      setStreet(addr.street);
      setNeighborhood(addr.neighborhood);
      setNumber(addr.number);
      setLatitude(lat);
      setLongitude(lon);
      setNeighborhoodOptions([]);
    } catch {
      setError('Não foi possível obter sua localização');
    } finally {
      setGeoLoading(false);
    }
  }

  async function HandleSubmit(e) {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      let lat = latitude;
      let lon = longitude;

      if (lat === null || lon === null) {
        const coords = await GeocodeFullAddress(street, number, neighborhood, city);
        if (!coords) throw new Error('Endereço não encontrado. Tente ser mais específico.');
        lat = coords.latitude;
        lon = coords.longitude;
      }

      const response = await fetch(`${API_URL}/pets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: status === 'lost' ? name : undefined,
          type,
          status,
          description: description || undefined,
          latitude: lat,
          longitude: lon,
          user_id: user.id,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? 'Erro ao criar postagem');
      }

      navigate('/feed', { state: { showMyPosts: true } });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  function HandleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <div className="create-post-container">
      <header className="create-post-header">
        <img src={logo} alt="OndeTá?" className="create-post-logo" />
        <div className="create-post-header-actions">
          <button className="create-post-nav-btn" onClick={() => navigate('/feed')}>
            Feed
          </button>
          <button className="create-post-nav-btn create-post-nav-btn--active">
            Criar postagem
          </button>
          <button className="create-post-nav-btn" onClick={() => navigate('/feed', { state: { showMyPosts: true } })}>
            Minhas postagens
          </button>
          <button className="create-post-nav-btn" onClick={() => navigate('/profile')}>
            Meu perfil
          </button>
          <button className="create-post-logout-btn" onClick={HandleLogout}>
            Sair
          </button>
        </div>
      </header>

      <main className="create-post-main">
        <div className="create-post-card">

          {step === 1 && (
            <>
              <h2 className="create-post-title">O que aconteceu?</h2>
              <div className="create-post-options">
                <button
                  type="button"
                  className={`create-post-option ${status === 'lost' ? 'create-post-option--selected' : ''}`}
                  onClick={() => setStatus('lost')}
                >
                  <span className="create-post-option-icon">🔍</span>
                  <span className="create-post-option-label">Perdi um animal</span>
                </button>
                <button
                  type="button"
                  className={`create-post-option ${status === 'found' ? 'create-post-option--selected' : ''}`}
                  onClick={() => setStatus('found')}
                >
                  <span className="create-post-option-icon">🐾</span>
                  <span className="create-post-option-label">Encontrei um animal</span>
                </button>
              </div>
              <button
                className="create-post-submit-btn"
                onClick={HandleContinue}
                disabled={!status}
              >
                Continuar
              </button>
            </>
          )}

          {step === 2 && (
            <>
              <h2 className="create-post-title">
                {status === 'lost' ? 'Perdi um animal' : 'Encontrei um animal'}
              </h2>

              <form onSubmit={HandleSubmit} className="create-post-form">
                {status === 'lost' && (
                  <div className="create-post-field">
                    <label htmlFor="name">Nome do animal</label>
                    <input
                      id="name"
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Ex: Rex"
                      required
                    />
                  </div>
                )}

                <div className="create-post-field">
                  <label htmlFor="type">Tipo</label>
                  <select
                    id="type"
                    value={type}
                    onChange={(e) => setType(e.target.value)}
                    required
                  >
                    <option value="">Selecione</option>
                    <option value="cachorro">Cachorro</option>
                    <option value="gato">Gato</option>
                  </select>
                </div>

                <div className="create-post-field">
                  <label htmlFor="description">Descrição</label>
                  <textarea
                    id="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder={status === 'lost' ? 'Descreva características do animal, local onde foi visto pela última vez...' : 'Descreva características do animal, local onde foi visto...'}
                    rows={4}
                  />
                </div>

                <div className="create-post-location">
                  <div className="create-post-location-header">
                    <span className="create-post-location-label">Localização</span>
                    <button
                      type="button"
                      className="create-post-geo-btn"
                      onClick={HandleGeolocate}
                      disabled={geoLoading}
                    >
                      {geoLoading ? 'Obtendo...' : 'Usar minha localização'}
                    </button>
                  </div>

                  <div className="create-post-field create-post-autocomplete">
                    <label htmlFor="city">Cidade</label>
                    <input
                      id="city"
                      type="text"
                      value={city}
                      onChange={HandleCityChange}
                      onBlur={() => setTimeout(() => setCityOptions([]), 150)}
                      placeholder="Ex: Curitiba"
                      required
                      autoComplete="off"
                    />
                    {cityOptions.length > 0 && (
                      <ul className="create-post-dropdown">
                        {cityOptions.map((opt, i) => (
                          <li
                            key={i}
                            className="create-post-dropdown-item"
                            onMouseDown={() => HandleSelectCity(opt)}
                          >
                            {opt.label}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>

                  <div className="create-post-row create-post-row--street">
                    <div className="create-post-field create-post-autocomplete">
                      <label htmlFor="street">Rua</label>
                      <input
                        id="street"
                        type="text"
                        value={street}
                        onChange={HandleStreetChange}
                        onBlur={() => setTimeout(() => setStreetOptions([]), 150)}
                        placeholder="Ex: Rua das Flores"
                        required
                        autoComplete="off"
                      />
                      {streetOptions.length > 0 && (
                        <ul className="create-post-dropdown">
                          {streetOptions.map((opt, i) => (
                            <li
                              key={i}
                              className="create-post-dropdown-item"
                              onMouseDown={() => HandleSelectStreet(opt)}
                            >
                              {opt}
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                    <div className="create-post-field">
                      <label htmlFor="number">
                        Número <span className="create-post-optional">(opcional)</span>
                      </label>
                      <input
                        id="number"
                        type="text"
                        value={number}
                        onChange={(e) => setNumber(e.target.value)}
                        placeholder="Ex: 123"
                        autoComplete="off"
                      />
                    </div>
                  </div>

                  <div className="create-post-field create-post-autocomplete">
                    <label htmlFor="neighborhood">Bairro</label>
                    <input
                      id="neighborhood"
                      type="text"
                      value={neighborhood}
                      onChange={(e) => { setNeighborhood(e.target.value); setLatitude(null); setLongitude(null); }}
                      onFocus={HandleNeighborhoodFocus}
                      onBlur={() => setTimeout(() => setNeighborhoodOptions([]), 150)}
                      placeholder="Ex: Centro"
                      required
                      autoComplete="off"
                    />
                    {neighborhoodOptions.length > 0 && (
                      <ul className="create-post-dropdown">
                        {neighborhoodOptions.map((opt, i) => (
                          <li
                            key={i}
                            className="create-post-dropdown-item"
                            onMouseDown={() => HandleSelectNeighborhood(opt)}
                          >
                            {opt}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>

                {error && <p className="create-post-error">{error}</p>}

                <button type="submit" className="create-post-submit-btn" disabled={isLoading}>
                  {isLoading ? 'Publicando...' : 'Publicar postagem'}
                </button>
                <button type="button" className="create-post-back-btn" onClick={() => setStep(1)}>
                  ← Voltar
                </button>
              </form>
            </>
          )}

        </div>
      </main>
    </div>
  );
}
