"""
Test script for signup backend
Run with: python test_signup.py
"""
from app import app, db
from auth_service import AuthService
from database import User


def test_signup_backend():
    """Test the signup functionality"""
    
    print("\n" + "="*60)
    print("🧪 Testing Crypto Marketplace Signup Backend")
    print("="*60 + "\n")
    
    with app.app_context():
        # Clear existing test data
        db.drop_all()
        db.create_all()
        
        print("✅ Database initialized\n")
        
        # Test 1: Signup new user
        print("📝 Test 1: Signup new user")
        print("-" * 40)
        success, msg, user = AuthService.signup_user(
            email='john@example.com',
            username='johndoe',
            password='SecurePass123!',
            full_name='John Doe',
            wallet_address='0x742d35Cc6634C0532925a3b844Bc7e7595f'
        )
        print(f"Status: {success}")
        print(f"Message: {msg}")
        if user:
            print(f"User: {user.to_dict()}\n")
        
        # Test 2: Attempt duplicate email
        print("📝 Test 2: Attempt duplicate email signup")
        print("-" * 40)
        success, msg, user = AuthService.signup_user(
            email='john@example.com',
            username='johndoe2',
            password='AnotherPass123!'
        )
        print(f"Status: {success}")
        print(f"Message: {msg}\n")
        
        # Test 3: Invalid password (too short)
        print("📝 Test 3: Invalid password (too short)")
        print("-" * 40)
        success, msg, user = AuthService.signup_user(
            email='jane@example.com',
            username='janedoe',
            password='Short1!'
        )
        print(f"Status: {success}")
        print(f"Message: {msg}\n")
        
        # Test 4: Invalid email format
        print("📝 Test 4: Invalid email format")
        print("-" * 40)
        success, msg, user = AuthService.signup_user(
            email='invalid-email',
            username='invaliduser',
            password='ValidPass123!'
        )
        print(f"Status: {success}")
        print(f"Message: {msg}\n")
        
        # Test 5: Successful second user signup
        print("📝 Test 5: Successful second user signup")
        print("-" * 40)
        success, msg, user = AuthService.signup_user(
            email='jane@example.com',
            username='janedoe',
            password='StrongPass123!',
            full_name='Jane Doe',
            wallet_address='0x1234567890abcdef'
        )
        print(f"Status: {success}")
        print(f"Message: {msg}")
        if user:
            print(f"User: {user.to_dict()}\n")
        
        # Test 6: Login with correct credentials
        print("📝 Test 6: Login with correct credentials")
        print("-" * 40)
        success, msg, user = AuthService.login_user(
            email='john@example.com',
            password='SecurePass123!'
        )
        print(f"Status: {success}")
        print(f"Message: {msg}\n")
        
        # Test 7: Login with wrong password
        print("📝 Test 7: Login with wrong password")
        print("-" * 40)
        success, msg, user = AuthService.login_user(
            email='john@example.com',
            password='WrongPassword123!'
        )
        print(f"Status: {success}")
        print(f"Message: {msg}\n")
        
        # Test 8: Get user by ID
        print("📝 Test 8: Get user by ID")
        print("-" * 40)
        user = AuthService.get_user_by_id(1)
        if user:
            print(f"Found User: {user.to_dict()}\n")
        
        # Test 9: Check total users in database
        print("📝 Test 9: Database statistics")
        print("-" * 40)
        total_users = User.query.count()
        print(f"Total users in database: {total_users}")
        all_users = User.query.all()
        for u in all_users:
            print(f"  - {u.username} ({u.email})\n")
        
        print("="*60)
        print("✅ All tests completed!")
        print("="*60 + "\n")


if __name__ == '__main__':
    test_signup_backend()
