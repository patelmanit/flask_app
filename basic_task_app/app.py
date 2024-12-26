# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.title}>'

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")

# Initialize database
init_db()

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username  # Store username in session
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    todos = Todo.query.filter_by(user_id=session['user_id']).order_by(Todo.created_date.desc()).all()
    return render_template('index.html', todos=todos, username=session.get('username'))

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    
    if title:
        new_todo = Todo(
            title=title,
            description=description,
            user_id=session['user_id']
        )
        db.session.add(new_todo)
        db.session.commit()
        flash('Task added successfully!')
    
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
@login_required
def complete(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        flash('Unauthorized access')
        return redirect(url_for('index'))
    
    todo.completed = not todo.completed
    db.session.commit()
    flash('Task status updated!')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != session['user_id']:
        flash('Unauthorized access')
        return redirect(url_for('index'))
    
    db.session.delete(todo)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)