import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { signOut } from "firebase/auth";
import { auth } from '../firebase';
import style from '../styles/TaskList.module.css'

const API_URL = "http://localhost:8080";

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [myMemberships, setMyMemberships] = useState([]);
  const [newTask, setNewTask] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

const membershipStatusMap = React.useMemo(() => {
  const map = {};
  // Add null check
  if (myMemberships && myMemberships.forEach) {
    myMemberships.forEach(membership => {
      if (membership && membership.taskId) {
        map[membership.taskId] = membership.status || 'none';
      }
    });
  }
  return map;
}, [myMemberships]);

  const renderTaskButton = (task) => {
    if (task.ownerId === auth.currentUser?.uid) {
      return (
        <button >
          Manage Task
        </button>
      );
    }

    const status = membershipStatusMap[task.id];

    switch (status) {
      case 'accepted':
        return (
          <button>
            Enter
          </button>
        );
      case 'pending':
        return (
          <div>
            Pending Approval
          </div>
        );
      case 'rejected':
        return (
          <span >
            Join Rejected
          </span>
        );
      default:
        return (
          <button onClick={() => handleJoin(task.id)}>
            Join
          </button>
        );
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);


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
      const response = await axios.get(`${API_URL}/api/tasks`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setTasks(response.data.tasks);
      const response2 = await axios.get(`${API_URL}/api/member_of`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setMyMemberships(response2.data.task_members);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching tasks:", error);
      console.log(tasks)

      setLoading(false);
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

  const handleCreate = async () => {
    const token = localStorage.getItem('authToken');
    try {
      const response = await axios.post(`${API_URL}/api/tasks`, {
        title: newTask.title,
        description: newTask.description
      },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setIsModalOpen(false);
      setNewTask({ title: '', description: '' });

    }
    catch (err) {
      console.error("Failed to create task:", err);
    }
  }

  const handleJoin = async (id) => {
    const token = localStorage.getItem('authToken');
    try {
      const response = await axios.post(`${API_URL}/api/join`, {
        taskId: id,
      },
        { headers: { Authorization: `Bearer ${token}` } }
      );
    }
    catch (err) {
      console.error("Failed to create task:", err);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className={style.container}>
      <div className={style.header}>
        <button onClick={handleLogout}>Logout</button>{/*if in mytasks then enter instead of join and be redirected and if joined then cannot give another join whatever*/}
        <h2 className='title'>Organize your tasks to reach the Moon</h2>
        <button onClick={() => { setIsModalOpen(true) }}>Create Task</button>
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


      <div className={style.content}>
        {tasks.map(task => (
          <div key={task.id} className={style.task}>
            <div>
              <h3>{task.title}</h3>
              <p>{task.description}</p>
            </div>
            {
              // <button onClick={() => handleJoin(task.id)}>Join</button>
              renderTaskButton(task)
            }
          </div>
        ))}

      </div>

    </div>
  );
}

export default TaskList;