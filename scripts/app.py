"""
Flask API Server for Crypto Marketplace Signup
Run with: python app.py
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database import db, User, UserProfile
from auth_service import AuthService
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///crypto_marketplace.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'crypto-marketplace-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)

# Create tables
with app.app_context():
    db.create_all()


# ==================== Auth Routes ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """
    User signup endpoint
    
    Request body:
    {
        "email": "user@example.com",
        "username": "username",
        "password": "SecurePass123!",
        "full_name": "Full Name (optional)",
        "wallet_address": "0x... (optional)"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'username', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Signup user
        success, message, user = AuthService.signup_user(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            full_name=data.get('full_name'),
            wallet_address=data.get('wallet_address')
        )
        
        if not success:
            return jsonify({'error': message}), 400
        
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': message,
            'user': user.to_dict(),
            'access_token': access_token
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    """
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        # Login user
        success, message, user = AuthService.login_user(
            email=data['email'],
            password=data['password']
        )
        
        if not success:
            return jsonify({'error': message}), 401
        
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': message,
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify JWT token and get current user"""
    try:
        user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'Token valid',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== User Routes ====================

@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user profile by ID"""
    try:
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        return jsonify({
            'user': user.to_dict(),
            'profile': profile.to_dict() if profile else {}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user profile"""
    try:
        current_user = get_jwt_identity()
        
        # Check authorization
        if current_user != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        success, message = AuthService.update_user_profile(user_id, **data)
        
        if not success:
            return jsonify({'error': message}), 400
        
        user = AuthService.get_user_by_id(user_id)
        return jsonify({
            'message': message,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/check-username/<username>', methods=['GET'])
def check_username(username):
    """Check if username is available"""
    try:
        user = User.query.filter_by(username=username).first()
        
        return jsonify({
            'available': user is None,
            'username': username
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/check-email/<email>', methods=['GET'])
def check_email(email):
    """Check if email is available"""
    try:
        user = User.query.filter_by(email=email).first()
        
        return jsonify({
            'available': user is None,
            'email': email
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Crypto Marketplace API'}), 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Crypto Marketplace Signup API',
        'version': '1.0.0',
        'endpoints': {
            'auth': [
                'POST /api/auth/signup',
                'POST /api/auth/login',
                'GET /api/auth/verify'
            ],
            'users': [
                'GET /api/users/<id>',
                'PUT /api/users/<id>',
                'GET /api/users/check-username/<username>',
                'GET /api/users/check-email/<email>'
            ]
        }
    }), 200


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting Crypto Marketplace API Server...")
    print("📝 Endpoints available at http://localhost:5000/api/")
    app.run(debug=True, host='0.0.0.0', port=5000)
