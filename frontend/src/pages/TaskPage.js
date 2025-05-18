import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { auth } from '../firebase';
import style from '../styles/TaskPage.module.css';

const API_URL = "http://localhost:8080";

function TaskPage() {
    const { taskId } = useParams();
    const [task, setTask] = useState(null);
    const [miniTasks, setMiniTasks] = useState([]);
    const [newMiniTask, setNewMiniTask] = useState({ title: '', description: '' });
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchTaskDetails();
    }, [taskId]);

    const fetchTaskDetails = async () => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await axios.get(`${API_URL}/api/tasks/${taskId}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            setTask(response.data.task);
            setMiniTasks(response.data.miniTasks || []);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching task details:", error);
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewMiniTask(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleCreateMiniTask = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('authToken');
        try {
            await axios.post(`${API_URL}/api/tasks/${taskId}/mini-tasks`, {
                title: newMiniTask.title,
                description: newMiniTask.description
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setIsModalOpen(false);
            setNewMiniTask({ title: '', description: '' });
            await fetchTaskDetails();
        } catch (err) {
            console.error("Failed to create mini-task:", err);
        }
    };

    const handleCompleteMiniTask = async (miniTaskId) => {
        const token = localStorage.getItem('authToken');
        try {
            await axios.post(`${API_URL}/api/tasks/${taskId}/mini-tasks/${miniTaskId}/complete`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            await fetchTaskDetails();
        } catch (err) {
            console.error("Failed to complete mini-task:", err);
        }
    };

    if (loading) return <div className={style.loading}>Loading...</div>;
    if (!task) return <div className={style.error}>Task not found</div>;

    return (
        <div className={style.container}>
            <div className={style.header}>
                <button onClick={() => window.location.href = '/tasks'}>Back to Tasks</button>
                <h2>{task.title}</h2>
                <button onClick={() => setIsModalOpen(true)}>Add Mini-Task</button>
            </div>

            <div className={style.content}>
                <div className={style.taskDescription}>
                    <h3>Task Description</h3>
                    <p>{task.description}</p>
                </div>

                <div className={style.miniTasksSection}>
                    <h3>Mini Tasks</h3>
                    <div className={style.miniTasksList}>
                        {miniTasks.map(miniTask => (
                            <div key={miniTask.id} className={style.miniTask}>
                                <div className={style.miniTaskInfo}>
                                    <h4>{miniTask.title}</h4>
                                    <p>{miniTask.description}</p>
                                </div>
                                <button
                                    className={miniTask.completed ? style.completed : style.complete}
                                    onClick={() => !miniTask.completed && handleCompleteMiniTask(miniTask.id)}
                                    disabled={miniTask.completed}
                                >
                                    {miniTask.completed ? 'Completed' : 'Complete'}
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {isModalOpen && (
                <div className={style.modalOverlay}>
                    <div className={style.modalContent}>
                        <h3>Create a New Mini-Task</h3>
                        <form onSubmit={handleCreateMiniTask}>
                            <label>
                                Title
                                <input
                                    type="text"
                                    name="title"
                                    value={newMiniTask.title}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Description
                                <textarea
                                    name="description"
                                    value={newMiniTask.description}
                                    onChange={handleInputChange}
                                />
                            </label>
                            <div className={style.modalButtons}>
                                <button type="submit">Save</button>
                                <button
                                    type="button"
                                    onClick={() => {
                                        setIsModalOpen(false);
                                        setNewMiniTask({ title: '', description: '' });
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

export default TaskPage;
