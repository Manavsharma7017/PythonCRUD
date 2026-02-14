import React, { useState, useEffect } from 'react';
import '../styles/TaskForm.css';

function TaskForm({ onSubmit, onCancel, initialData, isEditing }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title);
      setDescription(initialData.description);
    }
  }, [initialData]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!title.trim()) {
      setError('Task title is required');
      return;
    }

    setLoading(true);
    try {
      if (isEditing) {
        await onSubmit(initialData.id, title, description);
      } else {
        await onSubmit(title, description);
      }
    } catch (err) {
      setError('Failed to save task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h3>{isEditing ? 'Edit Task' : 'Create New Task'}</h3>
        <button
          type="button"
          className="btn-close"
          onClick={onCancel}
        >
          ✕
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="form-group">
        <label htmlFor="title">Task Title *</label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          maxLength={255}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description (optional)"
          maxLength={5000}
          rows={4}
        />
      </div>

      <div className="form-actions">
        <button
          type="submit"
          disabled={loading}
          className="btn-primary"
        >
          {loading ? 'Saving...' : isEditing ? 'Update Task' : 'Create Task'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="btn-secondary"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}

export default TaskForm;
