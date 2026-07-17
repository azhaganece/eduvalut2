// EduVault App - Main JavaScript Utilities

// Department Configuration
const departmentConfig = {
    'ECE': {
        title: 'Electronics & Communication Engineering',
        heroTitle: 'Welcome to ECE',
        subtitle: 'Innovating the Future of Electronics',
        primaryColor: '#3b82f6',
        secondaryColor: '#8b5cf6',
        theme: 'electronics',
        emoji: '⚡'
    },
    'MECH': {
        title: 'Mechanical Engineering',
        heroTitle: 'Welcome to Mechanical Engineering',
        subtitle: 'Building the Machines of Tomorrow',
        primaryColor: '#f59e0b',
        secondaryColor: '#ef4444',
        theme: 'mechanical',
        emoji: '⚙️'
    },
    'CSE': {
        title: 'Computer Science Engineering',
        heroTitle: 'Welcome to CSE',
        subtitle: 'Coding the Future',
        primaryColor: '#10b981',
        secondaryColor: '#3b82f6',
        theme: 'computers',
        emoji: '💻'
    },
    'IT': {
        title: 'Information Technology',
        heroTitle: 'Welcome to IT',
        subtitle: 'Transforming Through Technology',
        primaryColor: '#06b6d4',
        secondaryColor: '#3b82f6',
        theme: 'coding',
        emoji: '🌐'
    },
    'AI': {
        title: 'Artificial Intelligence & Machine Learning',
        heroTitle: 'Welcome to AI/ML',
        subtitle: 'Intelligence for the Future',
        primaryColor: '#8b5cf6',
        secondaryColor: '#ec4899',
        theme: 'aiml',
        emoji: '🤖'
    },
    'EEE': {
        title: 'Electrical & Electronics Engineering',
        heroTitle: 'Welcome to EEE',
        subtitle: 'Powering the World',
        primaryColor: '#fbbf24',
        secondaryColor: '#f59e0b',
        theme: 'electrical',
        emoji: '🔌'
    }
};

// Authentication Functions
function isAuthenticated() {
    return !!localStorage.getItem('token');
}

function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function getCurrentDepartment() {
    return localStorage.getItem('department') || 'CSE';
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('department');
    window.location.href = '/login';
}

// API Functions
async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(endpoint, {
        ...options,
        headers
    });

    if (response.status === 401) {
        logout();
        throw new Error('Unauthorized');
    }

    return response.json();
}

// Department Theme Application
function applyDepartmentTheme(deptCode) {
    const config = departmentConfig[deptCode] || departmentConfig['CSE'];
    document.documentElement.style.setProperty('--primary-color', config.primaryColor);
    document.documentElement.style.setProperty('--secondary-color', config.secondaryColor);
    return config;
}

// Utility Functions
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '400px';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initialize page based on authentication
function initializeAuthState() {
    const isAuth = isAuthenticated();
    const currentPage = window.location.pathname;

    // Redirect unauthenticated users away from protected pages
    if (!isAuth && (currentPage.includes('/dashboard'))) {
        window.location.href = '/login';
    }

    // Redirect authenticated users away from login page
    if (isAuth && currentPage.includes('/login')) {
        window.location.href = '/dashboard';
    }
}

// Department Navigation
function navigateToDepartment(deptCode) {
    localStorage.setItem('department', deptCode);
    window.location.href = `/dashboard?dept=${deptCode}`;
}

// Export for module usage (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        departmentConfig,
        isAuthenticated,
        getCurrentUser,
        getCurrentDepartment,
        logout,
        apiCall,
        applyDepartmentTheme,
        formatDate,
        showNotification,
        initializeAuthState,
        navigateToDepartment
    };
}
