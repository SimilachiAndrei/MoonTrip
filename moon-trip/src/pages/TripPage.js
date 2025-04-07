import React, { useState, useCallback, useEffect } from 'react';
import { GoogleMap, useLoadScript, Marker } from '@react-google-maps/api';
import { db } from '../firebase';
import { collection, addDoc } from 'firebase/firestore';
import config from '../config';

const mapContainerStyle = {
  width: '100%',
  height: '400px'
};

const center = {
  lat: 20.0,
  lng: 0.0
};

function TripPage() {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: config.map_api_key
  });

  const [user, setUser] = useState(null);
  const [gsiScriptLoaded, setGsiScriptLoaded] = useState(false);

  const [earthCoords, setEarthCoords] = useState(null);
  const [moonLat, setMoonLat] = useState('');
  const [moonLng, setMoonLng] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [weather, setWeather] = useState(null);
  const [loadingWeather, setLoadingWeather] = useState(false);
  const [weatherError, setWeatherError] = useState(null);


  useEffect(() => {
    if (gsiScriptLoaded || !config.google_client_id) return;

    const initializeGoogleSignIn = () => {
      try {
        window.google.accounts.id.initialize({
          client_id: config.google_client_id,
          callback: handleGoogleSignIn
        });

        window.google.accounts.id.renderButton(
          document.getElementById('googleSignInBtn'),
          { theme: 'outline', size: 'large' }
        );
      } catch (error) {
        console.error('Error initializing Google Sign-In:', error);
      }
    };

    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => {
      setGsiScriptLoaded(true);
      initializeGoogleSignIn();
    };
    document.head.appendChild(script);

    return () => {
      document.head.removeChild(script);
    };

  }, [gsiScriptLoaded]);

  const handleGoogleSignIn = (response) => {
    try {
      const credential = response.credential;
      const userData = parseJwt(credential);
      setUser(userData);
    } catch (error) {
      console.error('Error handling Google Sign-In:', error);
    }
  };

  const parseJwt = (token) => {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
    }
  };

  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    setStartDate(today);
    setEndDate(today);
  }, []);

  const fetchWeather = async (lat, lng) => {
    try {
      setLoadingWeather(true);
      setWeatherError(null);

      if (!config.weather_api_key) {
        throw new Error('Missing or invalid weather API key in configuration');
      }

      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${config.weather_api_key}&units=metric`
      );

      const data = await response.json();

      if (data.cod && data.cod !== 200) {
        throw new Error(data.message || 'Unknown API error');
      }

      setWeather(data);
    } catch (err) {
      console.error("Error fetching weather:", err);
      setWeatherError(`Weather error: ${err.message}`);
      setWeather(null);
    } finally {
      setLoadingWeather(false);
    }
  };


  const onMapClick = useCallback(async (e) => {
    const clickedCoords = {
      lat: e.latLng.lat(),
      lng: e.latLng.lng()
    };
    setEarthCoords(clickedCoords);
    await fetchWeather(clickedCoords.lat, clickedCoords.lng);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!user) {
      alert('Please sign in with Google first!');
      return;
    }

    if (!earthCoords || !moonLat || !moonLng || !startDate || !endDate) {
      alert('Please fill in all fields.');
      return;
    }

    try {
      await addDoc(collection(db, 'trips'), {
        earthCoords,
        moonCoords: { lat: parseFloat(moonLat), lng: parseFloat(moonLng) },
        startDate,
        endDate,
        destination: 'Earth to Moon',
        weatherAtDeparture: weather,
        userId: user.sub // Store Google's unique user ID
      });
      //calling the api to do the reuqest
      await fetch('/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to: 'cgamer788@gmail.com',
          name: 'Ionescu Antonio',
          startDate,
          endDate,
          earthCoords,
          moonCoords: { lat: parseFloat(moonLat), lng: parseFloat(moonLng) }
        })
      });

      alert('Trip added successfully and confirmation sent to email!');
    } catch (err) {
      console.error("Error adding trip:", err);
      alert('Failed to add trip.');
    }
  };


  if (loadError) return <p>Error loading map</p>;
  if (!isLoaded) return <p>Loading map...</p>;

  return (
    <div style={{ padding: '20px' }}>
      {/* Authentication Section */}
      <div style={{ position: 'absolute', top: '20px', right: '20px' }}>
        {!user ? (
          <div id="googleSignInBtn" />
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <img
              src={user.picture}
              alt="Profile"
              style={{ width: '30px', borderRadius: '50%' }}
            />
            <span>Hello, {user.given_name}</span>
            <button
              onClick={() => setUser(null)}
              style={{
                padding: '5px 10px',
                background: '#ff4444',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Sign Out
            </button>
          </div>
        )}
      </div>

      {/* Original Content */}
      <h1>Plan Your Rocket Trip</h1>
      <p>Click on the map to select your Earth destination</p>

      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        zoom={2}
        center={center}
        onClick={onMapClick}
      >
        {earthCoords && <Marker position={earthCoords} />}
      </GoogleMap>

      {earthCoords && (
        <div style={{ margin: '20px 0', padding: '15px', border: '1px solid #ddd', borderRadius: '5px' }}>
          <h3>Selected Location</h3>
          <p>Latitude: {earthCoords.lat.toFixed(4)}</p>
          <p>Longitude: {earthCoords.lng.toFixed(4)}</p>

          {loadingWeather && <p>Loading weather data...</p>}
          {weatherError && <p style={{ color: 'red' }}>{weatherError}</p>}
          {weather && !loadingWeather && (
            <div>
              <h3>Current Weather</h3>
              <p><strong>Location:</strong> {weather.name}</p>
              <p><strong>Temperature:</strong> {weather.main.temp}°C</p>
              <p><strong>Feels Like:</strong> {weather.main.feels_like}°C</p>
              <p><strong>Conditions:</strong> {weather.weather[0].main} ({weather.weather[0].description})</p>
              <p><strong>Humidity:</strong> {weather.main.humidity}%</p>
              <p><strong>Wind:</strong> {weather.wind.speed} m/s, {weather.wind.deg}°</p>
            </div>
          )}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ marginTop: '30px' }}>
        <h2>Moon Landing Coordinates</h2>
        <label>Latitude:
          <input
            type="number"
            step="any"
            value={moonLat}
            onChange={(e) => setMoonLat(e.target.value)}
            required
            style={{ marginLeft: '10px' }}
          />
        </label>
        <br />
        <label>Longitude:
          <input
            type="number"
            step="any"
            value={moonLng}
            onChange={(e) => setMoonLng(e.target.value)}
            required
            style={{ marginLeft: '10px' }}
          />
        </label>

        <h2>Time Period</h2>
        <label>Start Date:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
            style={{ marginLeft: '10px' }}
          />
        </label>
        <br />
        <label>End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            required
            style={{ marginLeft: '10px' }}
          />
        </label>

        <br /><br />
        <button type="submit" style={{ padding: '8px 16px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px' }}>
          Submit Trip
        </button>
      </form>
    </div>
  );
}

export default TripPage;
