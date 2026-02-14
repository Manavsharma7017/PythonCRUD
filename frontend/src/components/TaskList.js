import React from 'react';
import '../styles/TaskList.css';

function TaskList({ tasks, onEdit, onDelete, isAdmin }) {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="empty-state">
        <p>No tasks yet. Create one to get started!</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <div key={task.id} className="task-card">
          <div className="task-header">
            <h3>{task.title}</h3>
            <span className="task-id">#{task.id}</span>
          </div>

          {task.description && (
            <p className="task-description">{task.description}</p>
          )}

          <div className="task-meta">
            <span className="task-date">
              Created: {formatDate(task.created_at)}
            </span>
            {task.updated_at !== task.created_at && (
              <span className="task-date">
                Updated: {formatDate(task.updated_at)}
              </span>
            )}
          </div>

          <div className="task-actions">
            <button
              onClick={() => onEdit(task)}
              className="btn-edit"
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="btn-delete"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default TaskList;
