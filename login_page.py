"""
Simple Login Page Application
A basic command-line login system with user authentication
"""

import re
import hashlib
from pathlib import Path


class LoginSystem:
    """Simple login system with user management"""
    
    def __init__(self, users_file="users.txt"):
        self.users_file = users_file
        self.users = self.load_users()
    
    def load_users(self):
        """Load users from file"""
        users = {}
        if Path(self.users_file).exists():
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password_hash = line.strip().split(':')
                    users[username] = password_hash
        return users
    
    def save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            for username, password_hash in self.users.items():
                f.write(f"{username}:{password_hash}\n")
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, "Valid"
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        if not re.search("[a-z]", password):
            return False, "Password must contain lowercase letters"
        if not re.search("[A-Z]", password):
            return False, "Password must contain uppercase letters"
        if not re.search("[0-9]", password):
            return False, "Password must contain numbers"
        return True, "Valid"
    
    def register(self, username, password):
        """Register a new user"""
        # Validate username
        is_valid, message = self.validate_username(username)
        if not is_valid:
            return False, message
        
        # Check if user already exists
        if username in self.users:
            return False, "Username already exists"
        
        # Validate password
        is_valid, message = self.validate_password(password)
        if not is_valid:
            return False, message
        
        # Store user
        password_hash = self.hash_password(password)
        self.users[username] = password_hash
        self.save_users()
        return True, "Registration successful"
    
    def login(self, username, password):
        """Authenticate user"""
        if username not in self.users:
            return False, "User not found"
        
        password_hash = self.hash_password(password)
        if self.users[username] == password_hash:
            return True, "Login successful"
        else:
            return False, "Incorrect password"
    
    def delete_account(self, username, password):
        """Delete a user account"""
        is_authenticated, _ = self.login(username, password)
        if not is_authenticated:
            return False, "Authentication failed"
        
        del self.users[username]
        self.save_users()
        return True, "Account deleted successfully"


def display_menu():
    """Display main menu"""
    print("\n" + "="*40)
    print("     SIMPLE LOGIN SYSTEM")
    print("="*40)
    print("1. Register")
    print("2. Login")
    print("3. Delete Account")
    print("4. Exit")
    print("="*40)


def main():
    """Main application loop"""
    login_system = LoginSystem()
    current_user = None
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\n--- REGISTRATION ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            
            success, message = login_system.register(username, password)
            print(f"{'✓' if success else '✗'} {message}")
        
        elif choice == '2':
            print("\n--- LOGIN ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            
            success, message = login_system.login(username, password)
            if success:
                current_user = username
                print(f"✓ {message}")
                print(f"Welcome, {username}!")
            else:
                print(f"✗ {message}")
        
        elif choice == '3':
            if current_user is None:
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
            else:
                username = current_user
                password = input("Enter your password to confirm deletion: ").strip()
            
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm == 'yes':
                success, message = login_system.delete_account(username, password)
                print(f"{'✓' if success else '✗'} {message}")
                if success and current_user == username:
                    current_user = None
            else:
                print("Deletion cancelled")
        
        elif choice == '4':
            print("Thank you for using the login system. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
