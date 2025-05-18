import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { auth } from '../firebase';
import style from '../styles/TaskPage.module.css';

const API_URL = "http://localhost:8080";

const TASK_STATUS = {
    TODO: 'To Do',
    IN_PROGRESS: 'In Progress',
    COMPLETED: 'Completed'
};

const statusOrder = [TASK_STATUS.TODO, TASK_STATUS.IN_PROGRESS, TASK_STATUS.COMPLETED];

function TaskPage() {
    const { taskId } = useParams();
    const navigate = useNavigate();
    const [state, setState] = useState({
        task: null,
        miniTasks: [],
        error: null,
        loading: true
    });
    const [pendingUsers, setPendingUsers] = useState([]);
    const [currentUser, setCurrentUser] = useState(null);
    const [newMiniTask, setNewMiniTask] = useState({
        title: '',
        description: '',
        status: TASK_STATUS.TODO
    });
    const [isModalOpen, setIsModalOpen] = useState(false);

    const fetchPendingUsers = useCallback(async () => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await axios.get(`${API_URL}/api/tasks/${taskId}/pending-users`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setPendingUsers(response.data.pendingUsers || []);
        } catch (error) {
            console.error("Error fetching pending users:", error);
        }
    }, [taskId]);

    const fetchTaskDetails = useCallback(async () => {
        if (!taskId) {
            setState(prev => ({ ...prev, error: "No task ID found", loading: false }));
            return;
        }

        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setState(prev => ({ ...prev, error: "Please log in to view this task", loading: false }));
                return;
            }

            const response = await axios.get(`${API_URL}/api/tasks/${taskId}`, {
                headers: { Authorization: `Bearer ${token}` }
            });

            const taskData = response.data.task || response.data;
            if (!taskData) {
                setState(prev => ({ ...prev, error: "Task not found", loading: false }));
                return;
            }

            const miniTasksData = response.data.miniTasks || taskData.miniTasks || [];

            setState({
                task: taskData,
                miniTasks: Array.isArray(miniTasksData) ? miniTasksData : [],
                error: null,
                loading: false
            });

            // If current user is the owner, fetch pending users
            const user = auth.currentUser;
            setCurrentUser(user);
            if (user && taskData.ownerId === user.uid) {
                fetchPendingUsers();
            }

        } catch (error) {
            const errorMessage = error.response?.data?.message || error.message || "Error loading task";
            setState(prev => ({ ...prev, error: errorMessage, loading: false }));
            console.error("Error fetching task details:", error);
        }
    }, [taskId, fetchPendingUsers]);

    useEffect(() => {
        fetchTaskDetails();
    }, [fetchTaskDetails]);

    const handleUserAction = async (userId, action) => {
        const token = localStorage.getItem('authToken');
        try {
            await axios.post(
                `${API_URL}/api/tasks/${taskId}/user-action`,
                { 
                    userId,
                    action 
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            // Refresh pending users list
            fetchPendingUsers();
        } catch (err) {
            console.error(`Failed to ${action} user:`, err);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewMiniTask(prev => ({ ...prev, [name]: value }));
    };

    const handleCreateMiniTask = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('authToken');

        try {
            await axios.post(
                `${API_URL}/api/tasks/${taskId}/mini-tasks`,
                newMiniTask,
                { headers: { Authorization: `Bearer ${token}` } }
            );

            setIsModalOpen(false);
            setNewMiniTask({ title: '', description: '', status: TASK_STATUS.TODO });
            // Refetch task details to get the updated mini-tasks
            await fetchTaskDetails();

        } catch (err) {
            console.error("Failed to create mini-task:", err);
            // Revert on error by refetching the current state
            await fetchTaskDetails();
        }
    };

    const handleUpdateMiniTaskStatus = async (miniTaskId, newStatus) => {
        const token = localStorage.getItem('authToken');
        const taskToUpdate = state.miniTasks.find(task => task.id === miniTaskId);
        if (!taskToUpdate) return;

        // Optimistic UI update
        setState(prev => ({
            ...prev,
            miniTasks: prev.miniTasks.map(task =>
                task.id === miniTaskId ? { ...task, status: newStatus } : task
            )
        }));

        try {
            await axios.patch(
                `${API_URL}/api/tasks/${taskId}/mini-tasks/${miniTaskId}`,
                { status: newStatus },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            
            // Refetch task details to ensure consistency
            await fetchTaskDetails();
        } catch (err) {
            console.error("Failed to update mini-task status:", err);
            // Revert on error by refetching the current state
            await fetchTaskDetails();
        }
    };

    const handleDeleteMiniTask = async (miniTaskId) => {
        const token = localStorage.getItem('authToken');

        // Optimistic UI update
        setState(prev => ({
            ...prev,
            miniTasks: prev.miniTasks.filter(task => task.id !== miniTaskId)
        }));

        try {
            const response = await axios.delete(
                `${API_URL}/api/tasks/${taskId}/mini-tasks/${miniTaskId}`,
                { 
                    headers: { 
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    } 
                }
            );

            if (!response.data.success) {
                throw new Error('Failed to delete mini-task');
            }
        } catch (err) {
            console.error("Failed to delete mini-task:", err);
            // Revert on error by refetching the current state
            await fetchTaskDetails();
        }
    };

    const renderMiniTasksByStatus = (status) => {
        const filteredTasks = state.miniTasks.filter(task => task.status === status);

        return (
            <div className={style.miniTasksColumn}>
                <h3>{status}</h3>
                <div className={style.miniTasksList}>
                    {filteredTasks.length > 0 ? (
                        filteredTasks.map(miniTask => (
                            <div key={miniTask.id} className={style.miniTask}>
                                <div className={style.miniTaskInfo}>
                                    <h4>{miniTask.title}</h4>
                                    <p>{miniTask.description}</p>
                                </div>
                                <div className={style.miniTaskActions}>
                                    {status !== TASK_STATUS.COMPLETED && (
                                        <button
                                            className={style.complete}
                                            onClick={() => handleUpdateMiniTaskStatus(
                                                miniTask.id,
                                                status === TASK_STATUS.TODO ?
                                                    TASK_STATUS.IN_PROGRESS :
                                                    TASK_STATUS.COMPLETED
                                            )}
                                        >
                                            {status === TASK_STATUS.TODO ? 'Start' : 'Complete'}
                                        </button>
                                    )}
                                    <button
                                        className={style.delete}
                                        onClick={() => handleDeleteMiniTask(miniTask.id)}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className={style.emptyState}>
                            No tasks in {status.toLowerCase()}
                        </div>
                    )}
                </div>
            </div>
        );
    };

    const renderPendingUsers = () => {
        if (!currentUser || !state.task || state.task.ownerId !== currentUser.uid) {
            return null;
        }

        return (
            <div className={style.pendingUsersSection}>
                <h3>Pending Users</h3>
                <div className={style.pendingUsersList}>
                    {pendingUsers.length === 0 ? (
                        <div className={style.emptyState}>No pending users</div>
                    ) : (
                        pendingUsers.map(user => (
                            <div key={user.id} className={style.pendingUser}>
                                <span>{user.email}</span>
                                <div className={style.userActions}>
                                    <button
                                        className={style.accept}
                                        onClick={() => handleUserAction(user.id, 'accept')}
                                    >
                                        Accept
                                    </button>
                                    <button
                                        className={style.reject}
                                        onClick={() => handleUserAction(user.id, 'reject')}
                                    >
                                        Reject
                                    </button>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        );
    };

    if (state.loading) return <div className={style.loading}>Loading...</div>;
    if (state.error) return <div className={style.error}>{state.error}</div>;
    if (!state.task) return <div className={style.error}>Task not found</div>;

    return (
        <div className={style.container}>
            <div className={style.header}>
                <button onClick={() => navigate('/tasks')}>Back to Tasks</button>
                <h2>{state.task.title}</h2>
                <button onClick={() => setIsModalOpen(true)}>Add Mini-Task</button>
            </div>

            <div className={style.content}>
                <div className={style.taskDescription}>
                    <h3>Task Description</h3>
                    <p>{state.task.description || 'No description available'}</p>
                </div>

                {renderPendingUsers()}

                <div className={style.kanbanBoard}>
                    {statusOrder.map(status => renderMiniTasksByStatus(status))}
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
                            <label>
                                Status
                                <select
                                    name="status"
                                    value={newMiniTask.status}
                                    onChange={handleInputChange}
                                    required
                                >
                                    {Object.values(TASK_STATUS).map(status => (
                                        <option key={status} value={status}>{status}</option>
                                    ))}
                                </select>
                            </label>
                            <div className={style.modalButtons}>
                                <button type="button" onClick={() => setIsModalOpen(false)}>
                                    Cancel
                                </button>
                                <button type="submit">Save</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default TaskPage;