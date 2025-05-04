import React, { useState } from 'react';
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from '../firebase';
import axios from 'axios';

const API_URL = "http://localhost:8080"

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Firebase Authentication
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      const idToken = await user.getIdToken();
      
      // Store token for future API requests
      localStorage.setItem('authToken', idToken);
      
      // Update last login timestamp (optional)
      try {
        await axios.post(
          `${API_URL}/api/auth/login`,
          {},
          { headers: { Authorization: `Bearer ${idToken}` } }
        );
      } catch (serverError) {
        console.warn("Failed to update login timestamp:", serverError);
      }
      
      // Redirect
      window.location.href = '/tasks';
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="login-form">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <a href="/register">Register here</a>
      </p>
    </div>
  );
}

export default Login;