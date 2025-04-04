import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div style={{ padding: '40px', textAlign: 'center' }}>
      <h1>🌌 Welcome to Rocket Planner</h1>
      <p>Choose what you'd like to do:</p>

      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        gap: '20px', 
        marginTop: '30px' 
      }}>
        <Link 
          to="/plan" 
          style={{
            padding: '15px 30px',
            background: '#0066cc',
            color: '#fff',
            borderRadius: '8px',
            textDecoration: 'none',
            fontSize: '18px'
          }}
        >
          🛠️ Plan a New Trip
        </Link>

        <Link 
          to="/trips" 
          style={{
            padding: '15px 30px',
            background: '#00b894',
            color: '#fff',
            borderRadius: '8px',
            textDecoration: 'none',
            fontSize: '18px'
          }}
        >
          🚀 Browse Your Trips
        </Link>
      </div>
    </div>
  );
}

export default HomePage;
