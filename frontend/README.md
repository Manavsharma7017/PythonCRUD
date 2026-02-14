# Task Management Frontend

A modern React application for managing tasks with JWT authentication and role-based access control.

## Features

✅ **User Authentication** - Register and login with email/password  
✅ **JWT Token Management** - Secure token storage and validation  
✅ **Task CRUD Operations** - Create, read, update, delete tasks  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **Error Handling** - Clear error messages and user feedback  
✅ **Protected Routes** - Access control for authenticated users  
✅ **Role-Based Display** - Different features for user and admin roles  

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── api.js              # API client with axios
│   ├── pages/
│   │   ├── Login.js            # Login page
│   │   ├── Register.js         # Registration page
│   │   └── Dashboard.js        # Main dashboard
│   ├── components/
│   │   ├── TaskForm.js         # Task form component
│   │   ├── TaskList.js         # Task list component
│   │   └── ProtectedRoute.js   # Route protection
│   ├── styles/
│   │   ├── Auth.css            # Auth pages styling
│   │   ├── Dashboard.css       # Dashboard styling
│   │   ├── TaskForm.css        # Form styling
│   │   └── TaskList.css        # List styling
│   ├── App.js                  # Main app component
│   ├── App.css                 # App styles
│   ├── index.js                # Entry point
│   └── index.css               # Global styles
├── public/
│   └── index.html              # HTML template
├── package.json                # Dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites

- Node.js 14+
- npm or yarn
- Backend API running (see backend README)

### Installation

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
Created `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
```

3. **Start development server**
```bash
npm start
```

Application will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

Creates optimized production build in `build/` directory.

## Usage

### 1. Register New Account

1. Click "Register here" link on login page
2. Enter email, password, and full name
3. Submit form
4. Redirected to login page

### 2. Login

1. Enter registered email
2. Enter password
3. Click "Login"
4. Redirected to dashboard

### 3. Manage Tasks

**Create Task**
- Click "+ Create New Task" button
- Enter title and description
- Click "Create Task"

**View Tasks**
- All user's tasks displayed as cards
- Shows creation and update dates
- Display count of total tasks

**Edit Task**
- Click "Edit" button on task card
- Modify title and description
- Click "Update Task"

**Delete Task**
- Click "Delete" button on task card
- Confirm deletion
- Task removed immediately

### 4. Logout

- Click "Logout" button in top right
- Tokens cleared from storage
- Redirected to login page

## API Integration

### Authentication API

```javascript
import { authAPI } from './api/api';

// Register
authAPI.register(email, password, fullName);

// Login
authAPI.login(email, password);

// Get current user
authAPI.getCurrentUser();
```

### Tasks API

```javascript
import { tasksAPI } from './api/api';

// Get all tasks
tasksAPI.getTasks(skip, limit);

// Get single task
tasksAPI.getTask(taskId);

// Create task
tasksAPI.createTask(title, description);

// Update task
tasksAPI.updateTask(taskId, title, description);

// Delete task
tasksAPI.deleteTask(taskId);
```

## Token Management

### Storage

Tokens stored in browser's localStorage:
- `access_token` - JWT access token (30 min expiry)
- `refresh_token` - JWT refresh token (7 day expiry)

### Security

- Tokens sent with Authorization header: `Bearer <token>`
- Tokens cleared on logout
- Automatic logout on 401 (Unauthorized) responses
- Protected routes check token before rendering

## Error Handling

The application handles errors gracefully:

| Error | Handling |
|-------|----------|
| 400 Bad Request | Display validation error message |
| 401 Unauthorized | Logout and redirect to login |
| 403 Forbidden | Show permission error message |
| 404 Not Found | Show resource not found message |
| 500 Server Error | Display generic error message |

## Responsive Design

The application is responsive across devices:

- **Desktop** (1200px+) - Full-width layout with multi-column task grid
- **Tablet** (768px - 1199px) - Adjusted spacing and single column tasks
- **Mobile** (< 768px) - Stacked layout, full-width buttons

## Styling

### Global Styles (`index.css`)
- Font settings
- Color scheme
- Button styles
- Form styling
- Message styles

### Component Styles
- Auth pages (`Auth.css`)
- Dashboard (`Dashboard.css`)
- Task form (`TaskForm.css`)
- Task list (`TaskList.css`)

### Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Blue | #007bff |
| Success | Green | #28a745 |
| Danger | Red | #dc3545 |
| Secondary | Gray | #6c757d |
| Background | Light Gray | #f5f7fa |
| Border | Gray | #e0e0e0 |

## Performance Optimization

- Code splitting (React Router)
- Lazy loading components
- CSS minification
- Image optimization
- Gzip compression

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### Cannot connect to backend

1. Verify backend is running on port 8000
2. Check `REACT_APP_API_URL` in `.env`
3. Ensure CORS is enabled in backend
4. Check browser console for CORS errors

### Tokens not persisting

- Verify localStorage is enabled in browser
- Check browser privacy settings
- Clear browser cache and try again

### Login/Register not working

- Verify backend API is running
- Check network tab in developer tools
- Ensure correct email/password format
- Verify backend validation rules

## Development

### Available Scripts

```bash
# Start development server
npm start

# Run tests
npm test

# Build for production
npm build

# Eject configuration (irreversible)
npm eject
```

### Dependencies

- **react** - UI library
- **react-dom** - React DOM rendering
- **react-router-dom** - Client-side routing
- **axios** - HTTP client
- **react-scripts** - Build and test runner

### Project Configuration

- Create React App for rapid development
- ESLint for code quality
- Prettier for code formatting (optional)
- Jest for unit testing (optional)

## Future Enhancements

### Planned Features
- [ ] Task categories/tags
- [ ] Task priority levels
- [ ] Due dates and reminders
- [ ] Task assignments
- [ ] Comments and collaboration
- [ ] Dark mode
- [ ] Offline support (PWA)
- [ ] Mobile app (React Native)

### Technical Improvements
- [ ] Unit testing with Jest
- [ ] E2E testing with Cypress
- [ ] Redux for state management
- [ ] TypeScript support
- [ ] Storybook for components
- [ ] Performance monitoring

## Contributing

1. Create feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit changes (`git commit -m 'Add AmazingFeature'`)
3. Push to branch (`git push origin feature/AmazingFeature`)
4. Open Pull Request

## License

MIT License - See LICENSE file for details
