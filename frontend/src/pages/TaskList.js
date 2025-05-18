import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { signOut } from "firebase/auth";
import { auth } from '../firebase';
import style from '../styles/TaskList.module.css';
import { useNavigate } from 'react-router-dom';

const API_URL = "http://localhost:8080";

function TaskList() {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [myMemberships, setMyMemberships] = useState([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setCurrentUser(user);
      if (user) {
        fetchTasks();
      } else {
        navigate('/login');
      }
    });

    return () => unsubscribe();
  }, [navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewTask(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const [tasksResponse, membershipsResponse] = await Promise.all([
        axios.get(`${API_URL}/api/tasks`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API_URL}/api/member_of`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      setTasks(tasksResponse.data.tasks);
      setMyMemberships(membershipsResponse.data.my_tasks);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      localStorage.removeItem('authToken');
      navigate('/login');
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('authToken');
    try {
      await axios.post(
        `${API_URL}/api/tasks`,
        {
          title: newTask.title,
          description: newTask.description
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setIsModalOpen(false);
      setNewTask({ title: '', description: '' });
      fetchTasks();
    } catch (err) {
      console.error("Failed to create task:", err);
    }
  };

  const handleJoin = async (id) => {
    const token = localStorage.getItem('authToken');
    try {
      await axios.post(
        `${API_URL}/api/join`,
        { taskId: id },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchTasks();
    } catch (err) {
      console.error("Failed to join task:", err);
    }
  };

  const handleDeleteTask = async (taskId) => {
    const token = localStorage.getItem('authToken');

    // Optimistic UI update
    setTasks(prev => prev.filter(task => task.id !== taskId));

    try {
      const response = await axios.delete(
        `${API_URL}/api/tasks/${taskId}`,
        { 
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          } 
        }
      );

      if (!response.data.success) {
        throw new Error('Failed to delete task');
      }
    } catch (err) {
      console.error("Failed to delete task:", err);
      // Revert on error by refetching
      fetchTasks();
    }
  };

  const renderButtons = (task) => {
    if (!currentUser) return null;

    const buttons = [];

    if (task.status === 'completed') {
      buttons.push(
        <button key="completed" className={style.completeButton} disabled>
          Completed
        </button>
      );
    } else if (task.ownerId === currentUser.uid) {
      buttons.push(
        <button key="manage" onClick={() => navigate(`/task/${task.id}`)}>
          Manage Task
        </button>
      );
      buttons.push(
        <button 
          key="delete" 
          className={style.delete}
          onClick={() => handleDeleteTask(task.id)}
        >
          Delete Task
        </button>
      );
    } else {
      const membership = myMemberships.find(m => m.taskId === task.id);

      if (membership) {
        switch (membership.status) {
          case 'pending':
            buttons.push(
              <button key="pending" disabled>
                Pending Approval
              </button>
            );
            break;
          case 'accepted':
            buttons.push(
              <button key="enter" onClick={() => navigate(`/task/${task.id}`)}>
                Enter Task
              </button>
            );
            break;
          default:
            break;
        }
      } else {
        buttons.push(
          <button
            key="join"
            className={style.joinButton}
            onClick={() => handleJoin(task.id)}
          >
            Join Task
          </button>
        );
      }
    }

    return (
      <div className={style.taskButtons}>
        {buttons}
      </div>
    );
  };

  if (loading) {
    return (
      <div className={style.container}>
        <div className={style.header}>
          <button onClick={handleLogout}>Logout</button>
          <h2>Loading...</h2>
          <button disabled>Create Task</button>
        </div>
        <div className={style.content}>
          <div className={style.loading}>Loading tasks...</div>
        </div>
      </div>
    );
  }

  return (
    <div className={style.container}>
      <div className={style.header}>
        <button onClick={handleLogout}>Logout</button>
        <h2>Organize your tasks to reach the Moon</h2>
        <button onClick={() => setIsModalOpen(true)}>Create Task</button>
      </div>

      <div className={style.content}>
        {tasks.length === 0 ? (
          <div className={style.emptyState}>No tasks available. Create one to get started!</div>
        ) : (
          tasks.map(task => (
            <div key={task.id} className={style.task}>
              <div className={style.taskInfo}>
                <h3>{task.title}</h3>
                <p>{task.description}</p>
              </div>
              {renderButtons(task)}
            </div>
          ))
        )}
      </div>

      {isModalOpen && (
        <div className={style.modalOverlay}>
          <div className={style.modalContent}>
            <h3>Create a New Task</h3>
            <form onSubmit={handleCreate}>
              <label>
                Title
                <input
                  type="text"
                  name="title"
                  value={newTask.title}
                  onChange={handleInputChange}
                  required
                />
              </label>
              <label>
                Description
                <textarea
                  name="description"
                  value={newTask.description}
                  onChange={handleInputChange}
                />
              </label>
              <div className={style.modalButtons}>
                <button type="submit">Save</button>
                <button
                  type="button"
                  onClick={() => {
                    setIsModalOpen(false);
                    setNewTask({ title: '', description: '' });
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default TaskList;