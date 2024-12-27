from flask import render_template, request, redirect, url_for, session, flash
from models import db, User, Note

def init_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect(url_for('register'))
            
            user = User(username=username)
            user.set_password(request.form['password'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user:
            return redirect(url_for('login'))
        notes = Note.query.filter_by(user_id=user.id).all()
        return render_template('notes.html', notes=notes, username=user.username)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                return redirect(url_for('index'))
            flash('Invalid username or password')
            return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/add_note', methods=['POST'])
    def add_note():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        content = request.form['content']
        note = Note(content=content, user_id=session['user_id'])
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/delete_note/<int:note_id>')
    def delete_note(note_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        note = Note.query.get_or_404(note_id)
        if note.user_id != session['user_id']:
            return redirect(url_for('index'))
        
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))