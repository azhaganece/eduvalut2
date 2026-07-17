from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
basedir = os.path.abspath(os.path.dirname(__file__))
# Allow overriding the database via `DATABASE_URL` env var (Render/Postgres or other URL),
# otherwise use local sqlite file in `database/eduvault.db`.
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database", "eduvault.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')

# Ensure required directories exist
os.makedirs(os.path.join(basedir, 'database'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'video'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'code'), exist_ok=True)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    register_number = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='Student')
    is_active = db.Column(db.Boolean, default=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    
    def set_password(self, password):
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'register_number': self.register_number, 'role': self.role, 'is_active': self.is_active, 'department_id': self.department_id}

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    subjects = db.relationship('Subject', backref='department', lazy=True)
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'code': self.code, 'description': self.description}

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.Integer, nullable=True)
    credits = db.Column(db.Integer, nullable=True)
    faculty = db.Column(db.String(120), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    year = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'code': self.code, 'semester': self.semester, 'credits': self.credits, 'faculty': self.faculty, 'department_id': self.department_id, 'year': self.year, 'description': self.description}

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    material_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'material_type': self.material_type, 'description': self.description, 'file_path': self.file_path, 'subject_id': self.subject_id, 'uploader_id': self.uploader_id, 'status': self.status, 'is_featured': self.is_featured, 'created_at': self.created_at.isoformat() if self.created_at else None}

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'content': self.content, 'department_id': self.department_id, 'created_by': self.created_by, 'created_at': self.created_at.isoformat() if self.created_at else None}

# Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Allow a demo/master password for quick access during development.
        # NOTE: Remove or secure this in production.
        MASTER_PASSWORD = 'wyj'
        if password != MASTER_PASSWORD and not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 403
        
        token = create_access_token(identity=user.id)
        return jsonify({'access_token': token, 'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def me():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get user'}), 500

@app.route('/api/materials', methods=['GET'])
def list_materials():
    try:
        materials = Material.query.filter_by(status='approved').all()
        return jsonify([m.to_dict() for m in materials]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to load materials'}), 500

@app.route('/api/materials', methods=['POST'])
@jwt_required()
def create_material():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        subject_id = data.get('subject_id')
        if not subject_id:
            return jsonify({'error': 'Subject ID is required'}), 400
        
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        material = Material(
            title=title,
            material_type=data.get('material_type', 'pdf'),
            description=data.get('description', ''),
            subject_id=subject_id,
            uploader_id=user.id,
            status='approved' if user.role == 'Admin' else 'pending'
        )
        db.session.add(material)
        db.session.commit()
        return jsonify({'message': 'Material created', 'material': material.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create material'}), 500

@app.route('/api/subjects', methods=['GET'])
def list_subjects():
    try:
        subjects = Subject.query.all()
        return jsonify([s.to_dict() for s in subjects]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to load subjects'}), 500

@app.route('/api/departments', methods=['GET'])
def list_departments():
    try:
        departments = Department.query.all()
        return jsonify([d.to_dict() for d in departments]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to load departments'}), 500

@app.route('/api/announcements', methods=['GET'])
def list_announcements():
    try:
        announcements = Announcement.query.all()
        return jsonify([a.to_dict() for a in announcements]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to load announcements'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/login')
def login_page():
    return send_from_directory('.', 'login.html')

@app.route('/dashboard')
def dashboard_page():
    return send_from_directory('.', 'dashboard.html')

@app.route('/landing')
def landing_page():
    return send_from_directory('code', 'landing_base.html')

@app.route('/landing/<dept_code>')
def department_landing(dept_code):
    return send_from_directory('code', 'landing_base.html')

@app.route('/video/<path:filename>')
def serve_video(filename):
    try:
        video_path = os.path.join(basedir, 'video', filename)
        if os.path.exists(video_path):
            return send_from_directory(os.path.join(basedir, 'video'), filename, mimetype='video/mp4')
        else:
            print(f'Video file not found at: {video_path}')
            return jsonify({'error': 'Video not found'}), 404
    except Exception as e:
        print(f'Video serving error: {e}')
        return jsonify({'error': 'Failed to serve video'}), 500

@app.route('/<path:filename>')
def serve_static(filename):
    # Allow serving common static asset types (css, js, html, images)
    static_exts = ('.css', '.js', '.html', '.png', '.jpg', '.jpeg', '.svg', '.gif')
    if filename.endswith(static_exts):
        return send_from_directory('.', filename)
    return send_from_directory('.', 'index.html')

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return send_from_directory('.', 'index.html')

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

def seed_data():
    try:
        if User.query.count() == 0:
            admin = User(username='admin', email='admin@example.com', register_number='ADMIN001', role='Admin', is_active=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush()
        
        if Department.query.count() == 0:
            departments = [
                Department(name='Computer Science', code='CSE', description='Computer Science and Engineering'),
                Department(name='Electronics and Communication', code='ECE', description='Electronics and Communication Engineering'),
                Department(name='AI & Machine Learning', code='AI & ML', description='AI and ML'),
                Department(name='Information Technology', code='IT', description='Information Technology')
            ]
            db.session.add_all(departments)
            db.session.flush()
        
        if Subject.query.count() == 0:
            cse = Department.query.filter_by(code='CSE').first()
            if cse:
                subjects = [
                    Subject(name='Data Structures', code='CS101', semester=3, credits=4, faculty='Dr. Priya', department_id=cse.id, year='Second Year', description='Core DSA concepts'),
                    Subject(name='Operating Systems', code='CS201', semester=4, credits=4, faculty='Prof. Rahul', department_id=cse.id, year='Second Year', description='Operating systems fundamentals')
                ]
                db.session.add_all(subjects)
                db.session.flush()
        
        if Material.query.count() == 0:
            admin = User.query.filter_by(role='Admin').first()
            subject = Subject.query.first()
            if admin and subject:
                material = Material(title='Algorithms Notes', material_type='pdf', description='Comprehensive algorithm notes', subject_id=subject.id, uploader_id=admin.id, status='approved', is_featured=True)
                db.session.add(material)
                db.session.flush()
        
        if Announcement.query.count() == 0:
            admin = User.query.filter_by(role='Admin').first()
            dept = Department.query.first()
            if admin and dept:
                ann = Announcement(title='Welcome to EduVault', content='Explore a modern learning platform for college resources.', department_id=dept.id, created_by=admin.id)
                db.session.add(ann)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'Seeding error: {e}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(host=host, port=port, debug=debug)
