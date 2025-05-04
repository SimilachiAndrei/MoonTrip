import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { signOut } from "firebase/auth";
import { auth } from '../firebase';

const API_URL = "https://moontrip-455720.lm.r.appspot.com";

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.get(`${API_URL}/api/tasks`, {
        headers: { 
          Authorization: `Bearer ${token}` 
        }
      });
      setTasks(response.data.tasks);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching tasks:", error);
      setLoading(false);
    }
  };

  const addTask = async (e) => {
    e.preventDefault();
    if (!newTask.trim()) return;
    
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.post(
        `${API_URL}/api/tasks`, 
        { title: newTask },
        { headers: { Authorization: `Bearer ${token}` }}
      );
      
      setTasks([...tasks, response.data]);
      setNewTask('');
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="task-manager">
      <header>
        <h1>Task Manager</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </header>
      
      <form onSubmit={addTask} className="task-form">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Add a new task..."
        />
        <button type="submit">Add</button>
      </form>
      
      <div className="task-list">
        <h2>Your Tasks</h2>
        {tasks.length === 0 ? (
          <p>No tasks yet. Add some tasks to get started!</p>
        ) : (
          <ul>
            {tasks.map((task) => (
              <li key={task.id}>
                <span className={task.completed ? 'completed' : ''}>
                  {task.title}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default TaskList;