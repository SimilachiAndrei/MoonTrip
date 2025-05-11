import React, { useState } from 'react';
import { auth } from '../firebase';
import { createUserWithEmailAndPassword } from "firebase/auth";
import axios from 'axios';
import style from '../styles/Login.module.css'


const API_URL = "http://localhost:8080";

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      // 1. Create user in Firebase Auth
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      // 2. Get the token and make sure it's valid
      const idToken = await user.getIdToken(true);

      // 3. Save user data to backend
      try {
        await axios.post(
          `${API_URL}/api/users`,
          { email: email },
          {
            headers: {
              'Authorization': `Bearer ${idToken}`,
              'Content-Type': 'application/json'
            }
          }
        );
      } catch (backendError) {
        if (backendError.response?.data?.error?.includes("Token used too early")) {
          console.log("Ignoring clock synchronization error, continuing...");
        } else {
          throw backendError; 
        }
      }

      // 4. Redirect
      window.location.href = '/login';
    } catch (error) {
      console.error("Registration error:", error);
      setError(error.message);
    }
  };
  return (
    <div className={style.loginform}>
      <h2 className={style.title}>Register</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleRegister}>
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
        <button type="submit">Register</button>
      </form>
      <p>Already have an account?
        <a href='/login'>Login here</a>
      </p>
    </div>
  );
}

export default Register;