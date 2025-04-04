import React, { useState, useCallback } from 'react';
import { GoogleMap, useLoadScript, Marker } from '@react-google-maps/api';
import { db } from '../firebase';
import { collection, addDoc } from 'firebase/firestore';
import { map_api_key } from '../config'; 

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
    googleMapsApiKey: map_api_key
  });

  const [earthCoords, setEarthCoords] = useState(null);
  const [moonLat, setMoonLat] = useState('');
  const [moonLng, setMoonLng] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const onMapClick = useCallback((e) => {
    setEarthCoords({
      lat: e.latLng.lat(),
      lng: e.latLng.lng()
    });
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
        destination: 'Earth to Moon'
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

      <form onSubmit={handleSubmit} style={{ marginTop: '30px' }}>
        <h2>Moon Landing Coordinates</h2>
        <label>Latitude:
          <input
            type="number"
            step="any"
            value={moonLat}
            onChange={(e) => setMoonLat(e.target.value)}
            required
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
          />
        </label>

        <h2>Time Period</h2>
        <label>Start Date:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
          />
        </label>
        <br />
        <label>End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            required
          />
        </label>

        <br /><br />
        <button type="submit">Submit Trip</button>
      </form>
    </div>
  );
}

export default TripPage;
