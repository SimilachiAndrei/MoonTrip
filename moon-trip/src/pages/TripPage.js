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

  const [earthCoords, setEarthCoords] = useState(null);
  const [moonLat, setMoonLat] = useState('');
  const [moonLng, setMoonLng] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [weather, setWeather] = useState(null);
  const [loadingWeather, setLoadingWeather] = useState(false);
  const [weatherError, setWeatherError] = useState(null);

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
        weatherAtDeparture: weather
      });
      alert('Trip added successfully!');
    } catch (err) {
      console.error("Error adding trip:", err);
      alert('Failed to add trip.');
    }
  };

  if (loadError) return <p>Error loading map</p>;
  if (!isLoaded) return <p>Loading map...</p>;

  return (
    <div style={{ padding: '20px' }}>
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