import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TripPage from './pages/TripPage';

function App() {
  return (
    <div className="app">
      <nav>
        <Link to="/">Home</Link>
        <Link to="/trip">Plan Trip</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/trip" element={<TripPage />} />
      </Routes>
    </div>
  );
}

export default App;