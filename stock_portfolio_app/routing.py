from flask import render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User
import yfinance as yf

stocks = []

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
        return render_template('portfolio.html', stocks = stocks, username=user.username)

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

    @app.route('/search-stock')
    def search_stock():
        query = request.args.get('query', '').upper()
        if not query:
            return jsonify([])
        
        try:
            # Search for the stock using yfinance
            stock = yf.Ticker(query)
            info = stock.info
            
            # Return basic stock information
            return jsonify([{
                'symbol': query,
                'name': info.get('longName', ''),
                'currentPrice': info.get('currentPrice', 0),
                'currency': info.get('currency', 'USD')
            }])
        except:
            return jsonify([])

    @app.route('/add-stock', methods=['POST'])
    def add_stock():
        stock = {
            'id': len(stocks) + 1,
            'symbol': request.form['symbol'],
            'shares': float(request.form['shares']),
            'price': float(request.form['price'])
        }
        stocks.append(stock)
        return redirect('/')

    @app.route('/delete-stock/<int:id>', methods=['POST'])
    def delete_stock(id):
        global stocks
        stocks = [s for s in stocks if s['id'] != id]
        return redirect('/')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))