import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { signOut } from "firebase/auth";
import { auth } from '../firebase';

const API_URL = "http://localhost:8080";

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    subtasks: [{ name: '', description: '' }] // Initialize with one empty subtask
  });

  const handleSubtaskChange = (index, field, value) => {
    const updatedSubtasks = [...newTask.subtasks];
    updatedSubtasks[index][field] = value;
    setNewTask({ ...newTask, subtasks: updatedSubtasks });
  };

  const addSubtaskField = () => {
    setNewTask({
      ...newTask,
      subtasks: [...newTask.subtasks, { name: '', description: '' }]
    });
  };

  const removeSubtaskField = (index) => {
    const updatedSubtasks = [...newTask.subtasks];
    updatedSubtasks.splice(index, 1);
    setNewTask({ ...newTask, subtasks: updatedSubtasks });
  };


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

// In TaskList.js, modify the addTask function:
const addTask = async (e) => {
  e.preventDefault();
  if (!newTask.title.trim()) return;

  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.post(
      `${API_URL}/api/tasks`,
      {
        title: newTask.title,
        description: newTask.description,
        subtasks: newTask.subtasks 
      },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    setTasks([...tasks, response.data]);
    setNewTask({
      title: '',
      description: '',
      subtasks: [{ name: '', description: '' }]
    });
  } catch (error) {
    console.error("Error adding task:", error);
  }
};

  const deleteTask = async (taskId) => {
    try {
      const token = await auth.currentUser.getIdToken();
      const response = await axios.delete(
        `${API_URL}/api/tasks/${taskId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      // Refresh task list after deletion
      fetchTasks();
    } catch (error) {
      console.error('Delete error:', error.response?.data || error.message);
      alert(error.response?.data?.error || 'Failed to delete task');
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
        <div className="form-group">
          <input
            type="text"
            name="title"
            value={newTask.title}
            onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
            placeholder="Main task title"
            required
          />
        </div>

        <div className="form-group">
          <textarea
            name="description"
            value={newTask.description}
            onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
            placeholder="Main task description"
            rows="3"
          />
        </div>

        <div className="subtasks-section">
          <h4>Subtasks</h4>
          {newTask.subtasks.map((subtask, index) => (
            <div key={index} className="subtask-group">
              <input
                type="text"
                value={subtask.name}
                onChange={(e) => handleSubtaskChange(index, 'name', e.target.value)}
                placeholder="Subtask name"
              />
              <textarea
                value={subtask.description}
                onChange={(e) => handleSubtaskChange(index, 'description', e.target.value)}
                placeholder="Subtask description"
                rows="2"
              />
              {newTask.subtasks.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeSubtaskField(index)}
                  className="remove-subtask"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={addSubtaskField}
            className="add-subtask"
          >
            + Add Subtask
          </button>
        </div>

        <button type="submit">Create Task</button>
      </form>

      <div className="task-list">
        <h2>Your Tasks</h2>
        {tasks.length === 0 ? (
          <p>No tasks yet. Add some tasks to get started!</p>
        ) : (
          <ul className="task-list">
            {tasks.map((task) => (
              <li key={task.id} className="task-item">
                <div className="task-main">
                  <h3>{task.title}</h3>
                  {task.description && <p className="task-description">{task.description}</p>}
                  <button onClick={() => deleteTask(task.id)}>Delete Task</button>
                </div>

                {task.subtasks && task.subtasks.length > 0 && (
                  <ul className="subtask-list">
                    {task.subtasks.map((subtask, index) => (
                      <li key={index} className="subtask-item">
                        <strong>{subtask.name}</strong>
                        {subtask.description && <p>{subtask.description}</p>}
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default TaskList;