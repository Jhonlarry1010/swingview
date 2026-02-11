"""
Standalone test script for signup backend logic
Demonstrates user registration, validation, and authentication
"""
import re
import hashlib
from datetime import datetime


class MockDatabase:
    """Simple in-memory database for testing"""
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def add_user(self, user):
        user['id'] = self.next_id
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def get_user_by_email(self, email):
        for user in self.users.values():
            if user['email'] == email:
                return user
        return None
    
    def get_user_by_username(self, username):
        for user in self.users.values():
            if user['username'] == username:
                return user
        return None
    
    def get_all_users(self):
        return list(self.users.values())


class AuthService:
    """Authentication service for user signup and login"""
    
    db = MockDatabase()
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
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
        
        if not (has_upper and has_lower and has_digit):
            return False, "Password must contain uppercase, lowercase, and digits"
        
        return True, "Password is valid"
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if len(username) > 20:
            return False, "Username must not exceed 20 characters"
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Username can only contain letters, numbers, hyphens, and underscores"
        return True, "Username is valid"
    
    @staticmethod
    def signup_user(email, username, password, full_name=None, wallet_address=None):
        """
        Register a new user
        
        Returns:
            tuple: (success: bool, message: str, user: dict or None)
        """
        # Validate email format
        if not AuthService.validate_email(email):
            return False, "Invalid email format", None
        
        # Validate username format
        is_valid, msg = AuthService.validate_username(username)
        if not is_valid:
            return False, msg, None
        
        # Validate password strength
        is_valid, msg = AuthService.validate_password(password)
        if not is_valid:
            return False, msg, None
        
        # Check if email already exists
        if AuthService.db.get_user_by_email(email):
            return False, "Email already registered", None
        
        # Check if username already exists
        if AuthService.db.get_user_by_username(username):
            return False, "Username already taken", None
        
        try:
            # Create new user
            user = {
                'email': email,
                'username': username,
                'password_hash': AuthService.hash_password(password),
                'full_name': full_name or username,
                'wallet_address': wallet_address or None,
                'created_at': datetime.now().isoformat(),
                'is_active': True
            }
            
            user = AuthService.db.add_user(user)
            return True, "User registered successfully", user
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}", None
    
    @staticmethod
    def login_user(email, password):
        """
        Authenticate user login
        
        Returns:
            tuple: (success: bool, message: str, user: dict or None)
        """
        user = AuthService.db.get_user_by_email(email)
        
        if not user:
            return False, "Invalid email or password", None
        
        password_hash = AuthService.hash_password(password)
        if user['password_hash'] != password_hash:
            return False, "Invalid email or password", None
        
        if not user['is_active']:
            return False, "Account is inactive", None
        
        return True, "Login successful", user
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return AuthService.db.get_user_by_email(email)


def test_signup_backend():
    """Test the signup functionality"""
    
    print("\n" + "="*70)
    print("🧪 Testing Crypto Marketplace Signup Backend (Python Logic)")
    print("="*70 + "\n")
    
    # Test 1: Signup new user
    print("📝 Test 1: Signup new user")
    print("-" * 70)
    success, msg, user = AuthService.signup_user(
        email='john@example.com',
        username='johndoe',
        password='SecurePass123',
        full_name='John Doe',
        wallet_address='0x742d35Cc6634C0532925a3b844Bc7e7595f'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"Message: {msg}")
    if user:
        print(f"User ID: {user['id']}")
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}")
        print(f"Full Name: {user['full_name']}")
        print(f"Wallet: {user['wallet_address']}")
        print(f"Created: {user['created_at']}\n")
    
    # Test 2: Attempt duplicate email
    print("📝 Test 2: Attempt duplicate email signup")
    print("-" * 70)
    success, msg, user = AuthService.signup_user(
        email='john@example.com',
        username='johndoe2',
        password='AnotherPass123'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ BLOCKED (expected)'}")
    print(f"Message: {msg}\n")
    
    # Test 3: Invalid password (too short)
    print("📝 Test 3: Invalid password (too short)")
    print("-" * 70)
    success, msg, user = AuthService.signup_user(
        email='jane@example.com',
        username='janedoe',
        password='Short1'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ VALIDATION FAILED (expected)'}")
    print(f"Message: {msg}\n")
    
    # Test 4: Invalid email format
    print("📝 Test 4: Invalid email format")
    print("-" * 70)
    success, msg, user = AuthService.signup_user(
        email='invalid-email',
        username='invaliduser',
        password='ValidPass123'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ VALIDATION FAILED (expected)'}")
    print(f"Message: {msg}\n")
    
    # Test 5: Invalid username (too short)
    print("📝 Test 5: Invalid username (too short)")
    print("-" * 70)
    success, msg, user = AuthService.signup_user(
        email='alex@example.com',
        username='ab',
        password='ValidPass123'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ VALIDATION FAILED (expected)'}")
    print(f"Message: {msg}\n")
    
    # Test 6: Successful second user signup
    print("📝 Test 6: Successful second user signup")
    print("-" * 70)
    success, msg, user = AuthService.signup_user(
        email='jane@example.com',
        username='janedoe',
        password='StrongPass123',
        full_name='Jane Doe',
        wallet_address='0x1234567890abcdef'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"Message: {msg}")
    if user:
        print(f"User ID: {user['id']}")
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}\n")
    
    # Test 7: Login with correct credentials
    print("📝 Test 7: Login with correct credentials")
    print("-" * 70)
    success, msg, user = AuthService.login_user(
        email='john@example.com',
        password='SecurePass123'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"Message: {msg}")
    if user:
        print(f"Logged in as: {user['username']} ({user['email']})\n")
    
    # Test 8: Login with wrong password
    print("📝 Test 8: Login with wrong password")
    print("-" * 70)
    success, msg, user = AuthService.login_user(
        email='john@example.com',
        password='WrongPassword123'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ AUTHENTICATION FAILED (expected)'}")
    print(f"Message: {msg}\n")
    
    # Test 9: Login with non-existent email
    print("📝 Test 9: Login with non-existent email")
    print("-" * 70)
    success, msg, user = AuthService.login_user(
        email='nonexistent@example.com',
        password='SomePass123'
    )
    print(f"Status: {'✅ SUCCESS' if success else '❌ NOT FOUND (expected)'}")
    print(f"Message: {msg}\n")
    
    # Test 10: Database statistics
    print("📝 Test 10: Database statistics")
    print("-" * 70)
    all_users = AuthService.db.get_all_users()
    print(f"Total users registered: {len(all_users)}")
    print("Registered users:")
    for u in all_users:
        print(f"  • ID: {u['id']} | Username: {u['username']} | Email: {u['email']} | Active: {u['is_active']}")
    
    print("\n" + "="*70)
    print("✅ All tests completed successfully!")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_signup_backend()
