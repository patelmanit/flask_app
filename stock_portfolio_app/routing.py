from flask import request, session, jsonify
from flask_cors import cross_origin
from models import db, User, Stock  # Assuming you'll create a Stock model
import yfinance as yf

def init_routes(app):
    @app.route('/register', methods=['POST', 'OPTIONS'])
    @cross_origin(supports_credentials=True)
    def register():
        if request.method == 'OPTIONS':
            return jsonify({}), 200
            
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'message': 'Username and password required'}), 400
            
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({'message': 'Username already exists'}), 400
            
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            return jsonify({'message': 'Registration successful'}), 201
            
        except Exception as e:
            print("Registration error:", str(e))
            db.session.rollback()
            return jsonify({'message': f'Registration failed: {str(e)}'}), 500

    @app.route('/login', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return jsonify({
                'message': 'Login successful',
                'user': {'username': user.username}
            })
        return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/logout')
    @cross_origin(supports_credentials=True)
    def logout():
        session.clear()
        return jsonify({'message': 'Logged out'})

    @app.route('/search-stock')
    @cross_origin(supports_credentials=True)
    def search_stock():
        if 'user_id' not in session:
            print("User not authenticated")
            return jsonify({'message': 'Not authenticated'}), 401
            
        query = request.args.get('query', '').upper()
        print(f"Received query: {query}")
        
        if not query:
            print("Empty query received")
            return jsonify([])
            
        try:
            stock = yf.Ticker(query)
            info = stock.info
            print(f"Retrieved info for {query}: {info}")
            def get_current_price(symbol):
                ticker = yf.Ticker(symbol)
                todays_data = ticker.history(period='1d')
                return todays_data['Close'][0]
            
            result = [{
                'symbol': info['symbol'],
                'name': info.get('longName', ''),
                'currentPrice': get_current_price(info['symbol'])
            }]
            
            print(f"Returning result: {result}")
            return jsonify(result)
        except Exception as e:
            print(f"Stock search error for {query}: {str(e)}")
            return jsonify([])

    @app.route('/add-stock', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def add_stock():
        if 'user_id' not in session:
            return jsonify({'message': 'Not authenticated'}), 401
            
        data = request.get_json()
        symbol = data.get('symbol')
        shares = data.get('shares')
        price = data.get('price')
        
        if not all([symbol, shares, price]):
            return jsonify({'message': 'Missing required fields'}), 400
            
        try:
            stock = Stock(
                user_id=session['user_id'],
                symbol=symbol.upper(),
                shares=shares,
                price=price
            )
            db.session.add(stock)
            db.session.commit()
            
            return jsonify({
                'id': stock.id,
                'symbol': stock.symbol,
                'shares': stock.shares,
                'price': stock.price
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Failed to add stock: {str(e)}'}), 500

    @app.route('/delete-stock/<int:id>', methods=['POST'])
    @cross_origin(supports_credentials=True)
    def delete_stock(id):
        if 'user_id' not in session:
            return jsonify({'message': 'Not authenticated'}), 401
            
        try:
            stock = Stock.query.filter_by(id=id, user_id=session['user_id']).first()
            if not stock:
                return jsonify({'message': 'Stock not found'}), 404
                
            db.session.delete(stock)
            db.session.commit()
            return jsonify({'message': 'Stock deleted'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Failed to delete stock: {str(e)}'}), 500

    @app.route('/get-stocks')
    @cross_origin(supports_credentials=True)
    def get_stocks():
        if 'user_id' not in session:
            return jsonify({'message': 'Not authenticated'}), 401
            
        try:
            user_stocks = Stock.query.filter_by(user_id=session['user_id']).all()
            return jsonify([{
                'id': stock.id,
                'symbol': stock.symbol,
                'shares': stock.shares,
                'price': stock.price
            } for stock in user_stocks])
        except Exception as e:
            return jsonify({'message': f'Failed to fetch stocks: {str(e)}'}), 500