"""
Authentication Service for User Signup and Login
"""
from database import db, User, UserProfile
from datetime import datetime, timedelta
import re


class AuthService:
    """Service for handling user authentication"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        
        if not (has_upper and has_lower and has_digit):
            return False, "Password must contain uppercase, lowercase, and digits"
        
        return True, "Password is valid"
    
    @staticmethod
    def signup_user(email, username, password, full_name=None, wallet_address=None):
        """
        Register a new user
        
        Args:
            email: User email
            username: Unique username
            password: User password
            full_name: Optional full name
            wallet_address: Optional crypto wallet address
            
        Returns:
            tuple: (success: bool, message: str, user: User or None)
        """
        # Validate email format
        if not AuthService.validate_email(email):
            return False, "Invalid email format", None
        
        # Validate password strength
        is_valid, msg = AuthService.validate_password(password)
        if not is_valid:
            return False, msg, None
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return False, "Email already registered", None
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return False, "Username already taken", None
        
        try:
            # Create new user
            user = User(
                email=email,
                username=username,
                full_name=full_name,
                wallet_address=wallet_address
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Create default profile
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)
            db.session.commit()
            
            return True, "User registered successfully", user
            
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {str(e)}", None
    
    @staticmethod
    def login_user(email, password):
        """
        Authenticate user login
        
        Args:
            email: User email
            password: User password
            
        Returns:
            tuple: (success: bool, message: str, user: User or None)
        """
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return False, "Invalid email or password", None
        
        if not user.check_password(password):
            return False, "Invalid email or password", None
        
        return True, "Login successful", user
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def update_user_profile(user_id, **kwargs):
        """Update user profile information"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            
            allowed_fields = ['full_name', 'wallet_address']
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(user, key, value)
            
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            return True, "Profile updated successfully"
            
        except Exception as e:
            db.session.rollback()
            return False, f"Update failed: {str(e)}"
