# EduVault - Modern Academic Learning Platform

## Overview
EduVault is a professionally restructured education platform with department-specific themes, 3D motion effects, and responsive design. Built with HTML, CSS, JavaScript, and Python Flask backend.

## ✨ Features Implemented

### TASK 1: Backend Structure for Landing Pages
- **Unified Backend**: All landing pages now use a consistent backend structure
- **Database Integration**: Departments, subjects, materials, and announcements are managed through SQLAlchemy ORM
- **API Routes**: RESTful API endpoints for authentication and data retrieval

### TASK 2: Department-Specific Landing Pages with 3D Effects
Each department has its own unique theme with specific 3D motion animations:

| Department | Theme | Primary Color | 3D Effect | Emoji |
|------------|-------|--------------|-----------|-------|
| **CSE** | Computer Science | #10b981 | Rotating motion | 💻 |
| **ECE** | Electronics | #3b82f6 | Floating motion | ⚡ |
| **MECH** | Mechanical | #f59e0b | Pulse motion | ⚙️ |
| **IT** | Information Tech | #06b6d4 | Rotating motion | 🌐 |
| **AI** | Artificial Intelligence | #8b5cf6 | Floating motion | 🤖 |
| **EEE** | Electrical | #fbbf24 | Pulse motion | 🔌 |

**3D Motion Effects:**
- `motion-3d-rotate`: 360-degree rotation animation
- `motion-3d-float`: Smooth floating motion with rotation
- `motion-3d-pulse`: Scaling pulse effect

### TASK 3: College Logo & Login Page Redesign
- **Centralized Logo**: Logo is prominently centered on login page
- **Professional Design**: Glassmorphism effects with backdrop blur
- **High Visibility**: Large animated logo with pulse effect (140px × 140px)
- **Department Selection**: Students select their department during login
- **Dashboard Integration**: After login, redirects to department-specific dashboard

### TASK 4: Video Background & Welcome Page
- **Video Background**: Full-screen video background on all pages
- **Video Overlay**: Gradient overlay for better text readability
- **Fallback Animation**: Animated gradient if video fails to load
- **Responsive Video**: Video scales properly on all devices

## 📁 Project Structure

```
EduVault/
├── app.py                    # Flask backend with routes and API
├── index.html               # Welcome/Home page
├── login.html               # Login page with college logo
├── dashboard.html           # User dashboard (protected)
├── styles.css               # Centralized CSS with all themes
├── app.js                   # JavaScript utilities
├── requirements.txt         # Python dependencies
├── code/
│   └── landing_base.html   # Department landing page template
├── database/
│   └── eduvault.db         # SQLite database
└── video/
    └── background.mp4      # Background video
```

## 🎨 Design System

### Color Palette
- **Primary Colors**: Department-specific colors (gradient effects)
- **Background**: Dark blue gradient (#1a1a2e, #16213e, #0f3460)
- **Text**: White with opacity variations
- **Accents**: Secondary colors for each department

### Typography
- **Font Family**: Segoe UI, Tahoma, Geneva, Verdana
- **Headings**: Bold with gradient text effects
- **Body Text**: Regular weight with 1.6 line height

### Components
- **Cards**: Glassmorphic design with backdrop blur
- **Buttons**: Gradient backgrounds with hover effects
- **Forms**: Dark inputs with focus states
- **Badges**: Color-coded status indicators

## 🔐 Authentication Flow

```
1. User visits index.html (Welcome page)
   ↓
2. Selects department
   ↓
3. Navigates to /login
   ↓
4. Enters credentials and selects department
   ↓
5. API call to /api/auth/login
   ↓
6. Tokens stored in localStorage
   ↓
7. Redirects to /dashboard?dept=DEPT_CODE
   ↓
8. Dashboard loads department-specific content
```

## 🚀 API Endpoints

### Authentication
- `POST /api/auth/login` - Login with email and password
- `GET /api/auth/me` - Get current user info (requires JWT)

### Resources
- `GET /api/departments` - List all departments
- `GET /api/subjects` - List all subjects
- `GET /api/materials` - List all materials
- `GET /api/announcements` - List all announcements

## 💻 Frontend Pages

### index.html (Welcome Page)
- Hero section with department selection
- 6 department cards with unique emojis
- Feature highlights
- Call-to-action button

### login.html (Login Page)
- **Centralized College Logo** (highly visible)
- Email/Password input fields
- Department selector dropdown
- Demo credentials display
- JWT token handling

### dashboard.html (Protected Page)
- User welcome message
- Department-specific styles
- Statistics cards (materials, subjects, announcements)
- Dynamic content loading from API
- Logout button
- Responsive grid layout

## 🎯 Special Features

### 3D Motion Effects
All pages include department-specific 3D animations using CSS keyframes:
- Logo animations on every page
- Header floating effects
- Stats items floating animations
- Card hover transformations

### Responsive Design
- Mobile-first approach
- Breakpoints at 768px and 480px
- Flexible grid layouts
- Touch-friendly buttons

### Dark Theme
- Eye-friendly dark background
- High contrast text
- Gradient overlays
- Smooth animations

## 🔧 Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Platform**
   - Open browser: `http://localhost:5000`
   - Login with demo credentials:
     - Email: `admin@example.com`
     - Password: `admin123`

## 📊 Database Models

- **User**: Student/Admin with department association
- **Department**: 6 departments (CSE, ECE, MECH, IT, AI, EEE)
- **Subject**: Courses with faculty and credits
- **Material**: Course materials (PDFs, notes, assignments)
- **Announcement**: Department announcements

## 🎓 User Experience

### Welcome Page Flow
1. Land on beautiful welcome page with college logo
2. Choose department from 6 options
3. Each choice leads to login page
4. After authentication, access personalized dashboard

### Dashboard Experience
1. Greet user with name and department
2. Show relevant statistics
3. Display course materials
4. List subjects for the department
5. Show latest announcements
6. Easy logout option

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: Bcrypt password hashing
- **API**: RESTful with CORS support

## 📝 Notes

- All styling is centralized in `styles.css`
- No external CSS frameworks needed
- Clean, professional, simple structure
- Fully responsive design
- Proper error handling and validation
- Secure JWT authentication

## 🎉 Completed Tasks Summary

✅ **Task 1**: Landing pages with unified backend
✅ **Task 2**: Department-specific 3D motion effects
✅ **Task 3**: Centralized college logo on login page
✅ **Task 4**: Video background on all pages
✅ **Professional Structure**: Clean, simple HTML/CSS/JS only
✅ **Fully Functional**: All features working and tested

Enjoy your modern learning platform! 🚀
