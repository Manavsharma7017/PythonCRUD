import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { tasksAPI, authAPI } from '../api/api';
import TaskForm from '../components/TaskForm';
import TaskList from '../components/TaskList';
import '../styles/Dashboard.css';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const navigate = useNavigate();

  // Load user and tasks on mount
  useEffect(() => {
    loadUserAndTasks();
  }, []);

  const loadUserAndTasks = async () => {
    try {
      setLoading(true);
      const userResponse = await authAPI.getCurrentUser();
      setUser(userResponse.data);

      const tasksResponse = await tasksAPI.getTasks();
      setTasks(tasksResponse.data.tasks || []);
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        navigate('/login');
      } else {
        setError('Failed to load data. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (title, description) => {
    try {
      await tasksAPI.createTask(title, description);
      setSuccessMessage('Task created successfully!');
      setShowForm(false);
      loadUserAndTasks();
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError('Failed to create task. Please try again.');
    }
  };

  const handleUpdateTask = async (taskId, title, description) => {
    try {
      await tasksAPI.updateTask(taskId, title, description);
      setSuccessMessage('Task updated successfully!');
      setEditingTask(null);
      loadUserAndTasks();
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError('Failed to update task. Please try again.');
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await tasksAPI.deleteTask(taskId);
        setSuccessMessage('Task deleted successfully!');
        loadUserAndTasks();
        setTimeout(() => setSuccessMessage(''), 3000);
      } catch (err) {
        setError('Failed to delete task. Please try again.');
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Task Management Dashboard</h1>
          <div className="user-info">
            {user && (
              <>
                <span className="user-name">
                  Welcome, {user.full_name || user.email}!
                </span>
                <span className="user-role">{user.role}</span>
              </>
            )}
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-content">
        {error && <div className="error-message">{error}</div>}
        {successMessage && <div className="success-message">{successMessage}</div>}

        <div className="dashboard-controls">
          {!showForm && !editingTask && (
            <button
              onClick={() => setShowForm(true)}
              className="btn-primary"
            >
              + Create New Task
            </button>
          )}
        </div>

        {(showForm || editingTask) && (
          <TaskForm
            onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
            onCancel={() => {
              setShowForm(false);
              setEditingTask(null);
            }}
            initialData={editingTask}
            isEditing={!!editingTask}
          />
        )}

        <div className="tasks-section">
          <h2>Your Tasks ({tasks.length})</h2>
          <TaskList
            tasks={tasks}
            onEdit={setEditingTask}
            onDelete={handleDeleteTask}
            isAdmin={user?.role === 'admin'}
          />
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
