import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TripPage from './pages/TripPage';

function App() {
  return (
    <div className="app">
      
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/plan" element={<TripPage />} />
      </Routes>
    </div>
  );
}

export default App;